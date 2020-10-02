import logging

import ltr559
from blinker import signal


class LTR559:
    def __init__(self, address):
        logging.info('Initialising LTR559 sensor with address {}'.format(address))
        self._sensor = ltr559.LTR559(i2c_dev=address)

    def get_lux(self, mqtt_details):
        """
        Return measured lux from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring lux')
        lux = self._sensor.get_lux()
        logging.info('Broadcasting lux: {}'.format(lux))

        lux_signal = signal('lux')
        lux_signal.send(self, lux=lux, mqtt_topic=mqtt_details['topic'])
