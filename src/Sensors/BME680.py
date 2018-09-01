import bme680
import time
import logging
from blinker import signal


class BME680:
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
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_temperature(self, mqtt_details):
        """
        Return measured temperature from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
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
        temperature_signal.send(self, temperature=temperature, mqtt_topic=mqtt_details['topic'])

    def get_humidity(self, mqtt_details):
        """
        Return measured humidity from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
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
        humidity_signal.send(self, humidity=humidity, mqtt_topic=mqtt_details['topic'])

    def get_pressure(self, mqtt_details):
        """
        Return measured pressure from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
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
        pressure_signal.send(self, pressure=pressure, mqtt_topic=mqtt_details['topic'])

    def get_air_quality(self, mqtt_details):
        """
        Return measured air quality from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring air quality')
        if self._air_quality_baseline_calculated is False:
            logging.info('Sensor has no air quality baseline, calculating now')
            self._calculate_air_quality_baseline()

        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

        pending_measurement = True
        pending_count = 0
        air_quality = None
        gas_resistance = None
        hum_baseline = 40.0
        hum_weighting = 0.25

        start_time = time.time()
        current_time = time.time()
        sample_time = 45
        sample_data = []

        while current_time - start_time < sample_time:
            current_time = time.time()
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                sample_data.append(self._sensor.data.gas_resistance)
                time.sleep(1)

        self._sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)

        while pending_measurement and pending_count < 15:
            if self._sensor.get_sensor_data():
                gas_resistance = sum(sample_data[-20:]) / 20.0
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
        air_quality_signal.send(self, air_quality=air_quality, gas=gas_resistance, mqtt_topic=mqtt_details['topic'])

    def _calculate_air_quality_baseline(self):
        """
        Calculates the current baseline for the air quality sensor on the device.

        :return:
        """
        logging.debug('Calculating air quality baseline')
        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

        start_time = time.time()
        current_time = time.time()
        burn_in_time = 300
        burn_in_data = []

        while current_time - start_time < burn_in_time:
            current_time = time.time()
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                gas = self._sensor.data.gas_resistance
                burn_in_data.append(gas)
                time.sleep(1)

        self._gas_baseline = sum(burn_in_data[-50:]) / 50.0
        logging.info('Air quality baseline calculated: {}'.format(self._gas_baseline))
        self._air_quality_baseline_calculated = True
        self._sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
