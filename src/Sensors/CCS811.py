import logging
import time

from Adafruit_CCS811 import Adafruit_CCS811
from blinker import signal


class CCS811:

    BURN_IN_TIME_IN_SECONDS = 300
    AIR_QUALITY_SAMPLE_TIME_IN_SECONDS = 60

    def __init__(self, address):
        self._air_quality_baseline_calculated = False
        self._gas_baseline = None

        logging.debug('Initialising CCS811 sensor with address {}'.format(address))
        self._sensor = Adafruit_CCS811(address=address)

    def get_equivalent_co2(self, mqtt_details):
        """
        Return measured equivalent carbon dioxide from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
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
            time.sleep(0.5)

        logging.info('Broadcasting eCO2: {}'.format(eco2))
        eco2_signal = signal('eco2')
        eco2_signal.send(self, eco2=eco2, mqtt_topic=mqtt_details['topic'])

    def get_air_quality(self, mqtt_details):
        """
        Return measured air quality from the device.

        :param dict mqtt_details: Relevant details for publishing to the MQTT broker
        """
        logging.debug('Measuring air quality')

        if self._air_quality_baseline_calculated is False:
            logging.info('Sensor has no air quality baseline, calculating now')
            self._calculate_air_quality_baseline()

        hum_weighting = 0.25

        start_time = time.time()
        current_time = time.time()
        sample_data = []

        while current_time - start_time < CCS811.AIR_QUALITY_SAMPLE_TIME_IN_SECONDS:
            current_time = time.time()
            if self._sensor.getTVOC() and self._sensor.available():
                sample_data.append(self._sensor.getTVOC())
                time.sleep(1)

        gas_resistance = sum(sample_data[-35:]) / 35.0
        gas_offset = self._gas_baseline - gas_resistance

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            air_quality = (gas_resistance / self._gas_baseline) * (100 - (hum_weighting * 100))
        else:
            air_quality = 100 - (hum_weighting * 100)

        logging.info('Air quality received from sensor: {}'.format(air_quality))
        logging.info('Broadcasting air quality: {}'.format(air_quality))
        air_quality_signal = signal('air_quality')
        air_quality_signal.send(self, air_quality=air_quality, gas=gas_resistance, mqtt_topic=mqtt_details['topic'])

    def _calculate_air_quality_baseline(self):
        """
        Calculates the current baseline for the air quality sensor on the device.
        """
        logging.debug('Calculating air quality baseline')

        start_time = time.time()
        current_time = time.time()
        burn_in_data = []

        while current_time - start_time < CCS811.BURN_IN_TIME_IN_SECONDS:
            current_time = time.time()
            if self._sensor.getTVOC() and self._sensor.available():
                burn_in_data.append(self._sensor.getTVOC())
                time.sleep(1)

        self._gas_baseline = sum(burn_in_data[-50:]) / 50.0
        logging.info('Air quality baseline calculated: {}'.format(self._gas_baseline))
        self._air_quality_baseline_calculated = True
