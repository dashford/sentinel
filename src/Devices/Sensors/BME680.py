import bme680
import time
import logging
from blinker import signal


class BME680:

    BURN_IN_TIME_IN_SECONDS = 300
    AIR_QUALITY_SAMPLE_TIME_IN_SECONDS = 60
    COOL_DOWN_TEMPERATURE_DIFFERENCE = 0.25

    def __init__(self, address):
        logging.info('Initialising BME680 sensor with address {}'.format(address))

        if address == 0x77:
            address = bme680.I2C_ADDR_SECONDARY
            logging.debug('Using secondary address')
        else:
            address = bme680.I2C_ADDR_PRIMARY
            logging.debug('Using primary address')

        self._air_quality_baseline_calculated = False
        self._gas_baseline = None
        self._sensor = bme680.BME680(i2c_addr=address)
        self._sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_temperature(self):
        """
        Return measured temperature from the device.

        :return:
        """
        logging.debug('Measuring temperature')
        pending_measurement = True
        temperature = None

        if self._sensor.get_gas_status():
            logging.info('Air quality is currently being measured, skipping temperature measurement')
            return

        while pending_measurement:
            if self._sensor.get_sensor_data():
                temperature = self._sensor.data.temperature
                pending_measurement = False
                logging.info('Temperature received from sensor: {}'.format(temperature))
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

        logging.info('Broadcasting temperature: {}'.format(temperature))
        temperature_signal = signal('temperature')
        temperature_signal.send(self, temperature=temperature)

    def get_humidity(self):
        """
        Return measured humidity from the device.

        :return:
        """
        logging.debug('Measuring humidity')
        pending_measurement = True
        humidity = None

        if self._sensor.get_gas_status():
            logging.info('Air quality is currently being measured, skipping humidity measurement')
            return

        while pending_measurement:
            if self._sensor.get_sensor_data():
                humidity = self._sensor.data.humidity
                pending_measurement = False
                logging.info('Humidity received from sensor: {}'.format(humidity))
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

        logging.info('Broadcasting humidity: {}'.format(humidity))
        humidity_signal = signal('humidity')
        humidity_signal.send(self, humidity=humidity)

    def get_pressure(self):
        """
        Return measured pressure from the device.

        :return:
        """
        logging.debug('Measuring pressure')
        pending_measurement = True
        pressure = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                pressure = self._sensor.data.pressure
                pending_measurement = False
                logging.info('Pressure received from sensor: {}'.format(pressure))
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

        logging.info('Broadcasting pressure: {}'.format(pressure))
        pressure_signal = signal('pressure')
        pressure_signal.send(self, pressure=pressure)

    def get_air_quality(self):
        """
        Return measured air quality from the device.

        :return:
        """
        logging.debug('Measuring air quality')

        initial_temperature = None

        logging.debug('Measuring initial temperature and humidity readings')
        pending_measurement = True
        while pending_measurement:
            if self._sensor.get_sensor_data():
                initial_temperature = self._sensor.data.temperature
                pending_measurement = False
                logging.info('Temperature received from sensor: {}'.format(initial_temperature))
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

        if self._air_quality_baseline_calculated is False:
            logging.info('Sensor has no air quality baseline, calculating now')
            self._calculate_air_quality_baseline()

        pending_measurement = True
        pending_count = 0
        air_quality = None
        gas_resistance = None
        hum_baseline = 40.0
        hum_weighting = 0.25

        start_time = time.time()
        current_time = time.time()
        sample_data = []

        while current_time - start_time < BME680.AIR_QUALITY_SAMPLE_TIME_IN_SECONDS:
            current_time = time.time()
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                sample_data.append(self._sensor.data.gas_resistance)
                time.sleep(1)

        self._sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)

        while pending_measurement and pending_count < 15:
            if self._sensor.get_sensor_data():
                gas_resistance = sum(sample_data[-35:]) / 35.0
                gas_offset = self._gas_baseline - gas_resistance

                hum = self._sensor.data.humidity
                hum_offset = hum - hum_baseline

                # Calculate hum_score as the distance from the hum_baseline.
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
                else:
                    hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (gas_resistance / self._gas_baseline) * (100 - (hum_weighting * 100))
                else:
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                air_quality = hum_score + gas_score
                pending_measurement = False
                logging.info('Air quality received from sensor: {}'.format(air_quality))
            logging.debug('Sensor data not ready yet, will try again...')
            pending_count = pending_count + 1
            time.sleep(0.5)

        logging.info('Broadcasting air quality: {}'.format(air_quality))
        air_quality_signal = signal('air_quality')
        air_quality_signal.send(self, air_quality=air_quality, gas=gas_resistance)

        # Allow gas plate to cool down
        cooling = True
        while cooling:
            if self._sensor.get_sensor_data():
                if self._sensor.data.temperature <= initial_temperature + BME680.COOL_DOWN_TEMPERATURE_DIFFERENCE or initial_temperature is None:
                    cooling = False
                    logging.debug('Sensor has cooled down sufficiently')
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

    def _calculate_air_quality_baseline(self):
        """
        Calculates the current baseline for the air quality sensor on the device.

        :return:
        """
        logging.debug('Calculating air quality baseline')

        start_time = time.time()
        current_time = time.time()
        burn_in_data = []

        while current_time - start_time < BME680.BURN_IN_TIME_IN_SECONDS:
            current_time = time.time()
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                gas = self._sensor.data.gas_resistance
                burn_in_data.append(gas)
                time.sleep(1)

        self._gas_baseline = sum(burn_in_data[-50:]) / 50.0
        logging.info('Air quality baseline calculated: {}'.format(self._gas_baseline))
        self._air_quality_baseline_calculated = True
