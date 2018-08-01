import logging

import Adafruit_BME280
from blinker import signal


class BME280:
    def __init__(self, address):
        logging.debug('Initialising BME280 sensor with address {}'.format(address))
        self._sensor = Adafruit_BME280.BME280(address=address)

    def get_temperature(self, mqtt_details):
        """
        Return measured temperature from the device.

        :return:
        """
        logging.debug('Measuring temperature')
        temperature = self._sensor.read_temperature()
        logging.info('Returning temperature: {}'.format(temperature))

        temperature_signal = signal('temperature')
        temperature_signal.send(self, temperature=temperature, mqtt_topic=mqtt_details['topic'])

    def get_humidity(self, mqtt_details):
        """
        Return measured humidity from the device.

        :return float:
        """
        humidity = self._sensor.read_humidity()
        logging.info('Returning humidity: {}'.format(humidity))

        return humidity

    def get_pressure(self, mqtt_details):
        """
        Return measured pressure from the device.

        :return float:
        """
        pressure = self._sensor.read_pressure()
        logging.info('Returning pressure: {}'.format(pressure))

        return pressure
