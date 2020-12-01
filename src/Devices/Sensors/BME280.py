import logging

import Adafruit_BME280
from blinker import signal


class BME280:
    def __init__(self, address):
        logging.info('Initialising BME280 sensor with address {}'.format(address))
        self._sensor = Adafruit_BME280.BME280(address=address)

    def get_temperature(self):
        """
        Return measured temperature from the sensor.

        :return:
        """
        logging.debug('Measuring temperature')
        temperature = self._sensor.read_temperature()
        logging.info('Broadcasting temperature: {}'.format(temperature))

        temperature_signal = signal('temperature')
        temperature_signal.send(self, temperature=temperature)

    def get_humidity(self):
        """
        Return measured humidity from the sensor.

        :return:
        """
        logging.debug('Measuring humidity')
        humidity = self._sensor.read_humidity()
        logging.info('Broadcasting humidity: {}'.format(humidity))

        humidity_signal = signal('humidity')
        humidity_signal.send(self, humidity=humidity)

    def get_pressure(self):
        """
        Return measured pressure from the sensor.

        :return:
        """
        logging.debug('Measuring pressure')
        pressure = self._convert_to_hectopascals(pressure=self._sensor.read_pressure())
        logging.info('Broadcasting pressure: {}'.format(pressure))

        pressure_signal = signal('pressure')
        pressure_signal.send(self, pressure=pressure)

    def _convert_to_hectopascals(self, pressure):
        """
        Converts pressure to hectopascals

        :param float pressure:
        :return float:
        """
        return pressure / 100.0
