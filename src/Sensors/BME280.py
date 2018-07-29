import logging

import Adafruit_BME280


class BME280:
    def __init__(self, address):
        logging.debug('Initialising BME280 sensor with address {}'.format(address))
        self._sensor = Adafruit_BME280.BME280(address=address)

    def get_temperature(self):
        """
        Return measured temperature from the device.

        :return float:
        """
        temperature = self._sensor.read_temperature()
        logging.info('Returning temperature: {}'.format(temperature))

        return temperature

    def get_humidity(self):
        """
        Return measured humidity from the device.

        :return float:
        """
        humidity = self._sensor.read_humidity()
        logging.info('Returning humidity: {}'.format(humidity))

        return humidity

    def get_pressure(self):
        """
        Return measured pressure from the device.

        :return float:
        """
        pressure = self._sensor.read_pressure()
        logging.info('Returning pressure: {}'.format(pressure))

        return pressure
