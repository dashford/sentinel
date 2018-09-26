import logging

import Adafruit_BME280
from blinker import signal


class BME280:
    def __init__(self, address):
        logging.info('Initialising BME280 sensor with address {}'.format(address))
        self._sensor = Adafruit_BME280.BME280(address=address)

    def get_temperature(self, mqtt_details):
        """
        Return measured temperature from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring temperature')
        temperature = self._sensor.read_temperature()
        logging.info('Broadcasting temperature: {}'.format(temperature))

        temperature_signal = signal('temperature')
        temperature_signal.send(self, temperature=temperature, mqtt_topic=mqtt_details['topic'])

    def get_humidity(self, mqtt_details):
        """
        Return measured humidity from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring humidity')
        humidity = self._sensor.read_humidity()
        logging.info('Broadcasting humidity: {}'.format(humidity))

        humidity_signal = signal('humidity')
        humidity_signal.send(self, humidity=humidity, mqtt_topic=mqtt_details['topic'])

    def get_pressure(self, mqtt_details):
        """
        Return measured pressure from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring pressure')
        pressure = self._sensor.read_pressure() / 100.0
        logging.info('Broadcasting pressure: {}'.format(pressure))

        pressure_signal = signal('pressure')
        pressure_signal.send(self, pressure=pressure, mqtt_topic=mqtt_details['topic'])
