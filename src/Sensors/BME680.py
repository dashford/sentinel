import bme680
import time


class BME680:
    def __init__(self):
        self._sensor = bme680.BME680()
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_temperature(self, mqtt_client, event_dispatcher, mqtt_details):
        pending_measurement = True
        temperature = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                temperature = self._sensor.data.temperature
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = '{"temperature": {0:.2f}}'

        mqtt_client.publish(mqtt_details['topic'], temperature)
