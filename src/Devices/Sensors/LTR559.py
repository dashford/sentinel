import logging

import ltr559
from blinker import signal


class LTR559:
    def __init__(self, address):
        logging.info('Initialising LTR559 sensor with address {}'.format(address))
        self._sensor = ltr559.LTR559()

    def get_lux(self):
        """
        Return measured lux from the sensor.

        :return:
        """
        logging.debug('Measuring lux')
        lux = self._sensor.get_lux()
        logging.info('Broadcasting lux: {}'.format(lux))

        lux_signal = signal('lux')
        lux_signal.send(self, lux=lux)
