import bme680
import time
import json
import logging
from blinker import signal

from src.Event.EventDispatcher import EventDispatcher


class BME680:
    def __init__(self, address):
        logging.debug('Initialising BME680 sensor with address {}'.format(address))

        if address == 0x77:
            address = bme680.I2C_ADDR_SECONDARY
            logging.debug('Using secondary address')
        else:
            address = bme680.I2C_ADDR_PRIMARY
            logging.debug('Using primary address')

        self._sensor = bme680.BME680(i2c_addr=address)
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_temperature(self, mqtt_client, event_dispatcher, mqtt_details):
        """
        Return measured temperature from the device.

        :param mqtt_client:
        :param EventDispatcher event_dispatcher:
        :param dict mqtt_details: Details of the metric from user configuration
        :return:
        """
        logging.debug('Measuring temperature')
        pending_measurement = True
        temperature = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                temperature = self._sensor.data.temperature
                pending_measurement = False
                logging.info('Temperature received from sensor: {}'.format(temperature))
            logging.debug('Sensor data not ready yet, will try again...')
            time.sleep(0.5)

        logging.info('Publishing signal for temperature data')
        temperature_signal = signal('temperature')
        temperature_signal.send(self, temperature=temperature, mqtt_topic=mqtt_details['topic'])

        # message = Message()
        # message_formatter = JsonFormatter()
        # message.add_key_value(key='temperature', value=temperature)
        # message.add_key_value(key='success', value=True)
        #
        # logging.info('Publishing message for _get_temperature to MQTT broker')
        # mqtt_client.publish(metric_details['mqtt']['topic'], message_formatter.format(message=message.get_message()))
        #
        # logging.info('Dispatching temperature event')
        # event = TemperatureEvent(event_details=message)
        # event_dispatcher.dispatch(event_name=EventDispatcher.TEMPERATURE_SAVED, event=event)

    def get_humidity(self, mqtt_client, event_dispatcher, mqtt_details):
        pending_measurement = True
        humidity = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                humidity = self._sensor.data.humidity
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "humidity": humidity
        }

        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))

    def get_pressure(self, mqtt_client, event_dispatcher, mqtt_details):
        pending_measurement = True
        pressure = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                pressure = self._sensor.data.pressure
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "pressure": pressure
        }

        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))

    def get_air_quality(self, mqtt_client, event_dispatcher, mqtt_details):
        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

        pending_measurement = True
        air_quality = None
        start_time = time.time()
        current_time = time.time()
        burn_in_time = 60
        burn_in_data = []

        while current_time - start_time < burn_in_time:
            current_time = time.time()
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                gas = self._sensor.data.gas_resistance
                burn_in_data.append(gas)
                time.sleep(1)

        gas_baseline = sum(burn_in_data[-50:]) / 50.0
        hum_baseline = 40.0
        hum_weighting = 0.25

        while pending_measurement:
            if self._sensor.get_sensor_data() and self._sensor.data.heat_stable:
                gas = self._sensor.data.gas_resistance
                gas_offset = gas_baseline - gas

                hum = self._sensor.data.humidity
                hum_offset = hum - hum_baseline

                # Calculate hum_score as the distance from the hum_baseline.
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
                else:
                    hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))
                else:
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                air_quality = hum_score + gas_score
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "air_quality": air_quality
        }
        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))
        self._sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
