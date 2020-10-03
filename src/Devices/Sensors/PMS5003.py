import logging

import pms5003
from blinker import signal


class PMS5003:
    def __init__(self, address):
        logging.info('Initialising PMS5003 sensor with address {}'.format(address))
        self._sensor = pms5003.PMS5003(device=address)

    def get_pm_1_0_ug_m3(self, mqtt_details):
        """
        Return measured PM1.0 ug/m3 from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring PM1.0 ug/m3')
        data = self._sensor.read()
        pm = data.pm_ug_per_m3(size=1.0, atmospheric_environment=True)
        logging.info('Broadcasting PM1.0 ug/m3: {}'.format(pm))

        pm1_0_signal = signal('pm1.0_ug/m3')
        pm1_0_signal.send(self, pm=pm, mqtt_topic=mqtt_details['topic'])

    def get_pm_2_5_ug_m3(self, mqtt_details):
        """
        Return measured PM2.5 ug/m3 from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring PM2.5 ug/m3')
        data = self._sensor.read()
        pm = data.pm_ug_per_m3(size=2.5, atmospheric_environment=True)
        logging.info('Broadcasting PM2.5 ug/m3: {}'.format(pm))

        pm2_5_signal = signal('pm2.5_ug/m3')
        pm2_5_signal.send(self, pm=pm, mqtt_topic=mqtt_details['topic'])

    def get_pm_10_ug_m3(self, mqtt_details):
        """
        Return measured PM10 ug/m3 from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring PM10 ug/m3')
        data = self._sensor.read()
        pm = data.pm_ug_per_m3(size=None, atmospheric_environment=True)
        logging.info('Broadcasting PM10 ug/m3: {}'.format(pm))

        pm10_signal = signal('pm10.0_ug/m3')
        pm10_signal.send(self, pm=pm, mqtt_topic=mqtt_details['topic'])