import logging
from time import sleep

from Adafruit_CCS811 import Adafruit_CCS811
from blinker import signal


class CCS811:
    def __init__(self, address):
        logging.debug('Initialising CCS811 sensor with address {}'.format(address))
        self._sensor = Adafruit_CCS811(address=address)

    def get_equivalent_co2(self, mqtt_details):
        """
        Return measured equivalent carbon dioxide from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return float:
        """
        logging.debug('Measuring equivalent CO2')
        eco2 = None
        pending_measurement = True

        while pending_measurement:
            if self._sensor.available():
                eco2 = self._sensor.geteCO2()
                pending_measurement = False
                logging.info('eCO2 received from sensor: {}'.format(eco2))
            logging.debug('Sensor data not ready yet, will try again...')
            sleep(0.5)

        logging.info('Broadcasting eCO2: {}'.format(eco2))
        temperature_signal = signal('eco2')
        temperature_signal.send(self, eco2=eco2, mqtt_topic=mqtt_details['topic'])

    def get_air_quality(self):
        """
        Return measured air quality from the device.

        :return float:
        """
        air_quality = self._sensor.getTVOC()
        logging.info('Returning air_quality: {}'.format(air_quality))

        return air_quality
