import logging
from time import sleep

import pms5003
from blinker import signal


class PMS5003:
    def __init__(self, address):
        logging.info('Initialising PMS5003 sensor with address {}'.format(address))
        self._sensor = pms5003.PMS5003(device=address)

    def get_particulate_matter(self, mqtt_details):
        """
        Return measured PM1.0 ug/m3 from the sensor.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        :return:
        """
        logging.debug('Measuring particulate matter')
        pm1_0 = []
        pm2_5 = []
        pm10_0 = []
        for x in range(0, 15):
            data = self._sensor.read()
            pm1_0.append(data.pm_ug_per_m3(size=1.0, atmospheric_environment=False))
            pm2_5.append(data.pm_ug_per_m3(size=2.5, atmospheric_environment=False))
            pm10_0.append(data.pm_ug_per_m3(size=None, atmospheric_environment=False))
            sleep(1)

        avg_1_0 = sum(pm1_0) / len(pm1_0)
        avg_2_5 = sum(pm2_5) / len(pm2_5)
        avg_10_0 = sum(pm10_0) / len(pm10_0)

        logging.info('Broadcasting pm1.0_ug/m3: {}'.format(avg_1_0))
        pm1_0_signal = signal('pm1.0_ug/m3')
        pm1_0_signal.send(self, pm=avg_1_0, mqtt_topic=mqtt_details['topic'] + '/1.0')

        logging.info('Broadcasting pm2.5_ug/m3: {}'.format(avg_2_5))
        pm2_5_signal = signal('pm2.5_ug/m3')
        pm2_5_signal.send(self, pm=avg_2_5, mqtt_topic=mqtt_details['topic'] + '/2.5')

        logging.info('Broadcasting pm10.0_ug/m3: {}'.format(avg_10_0))
        pm10_0_signal = signal('pm10.0_ug/m3')
        pm10_0_signal.send(self, pm=avg_10_0, mqtt_topic=mqtt_details['topic'] + '/10.0')
