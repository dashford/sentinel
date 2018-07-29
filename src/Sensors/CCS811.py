import logging
from time import sleep

from Adafruit_CCS811 import Adafruit_CCS811


class CCS811:
    def __init__(self, address):
        logging.debug('Initialising CCS811 sensor with address {}'.format(address))
        self._sensor = Adafruit_CCS811(address=address)

    def get_equivalent_co2(self):
        """
        Return measured equivalent carbon dioxide from the device.

        :return float:
        """
        eco2 = None
        pending_measurement = True

        while pending_measurement:
            if self._sensor.available():
                eco2 = self._sensor.geteCO2()
                pending_measurement = False
            sleep(0.5)

        logging.info('Returning eco2: {}'.format(eco2))

        return eco2

    def get_air_quality(self):
        """
        Return measured air quality from the device.

        :return float:
        """
        air_quality = self._sensor.getTVOC()
        logging.info('Returning air_quality: {}'.format(air_quality))

        return air_quality
