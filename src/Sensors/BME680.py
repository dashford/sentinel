import bme680
import time
import json

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Events.TemperatureEvent import TemperatureEvent


class BME680:
    def __init__(self):
        self._sensor = bme680.BME680()
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)

    def get_temperature(self, mqtt_client, event_dispatcher, mqtt_details):
        """
        Return the temperature.

        :param mqtt_client:
        :param EventDispatcher event_dispatcher:
        :param dict mqtt_details: Details of MQTT specifics from user configuration
        :return:
        """
        pending_measurement = True
        temperature = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                temperature = self._sensor.data.temperature
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "temperature": temperature
        }

        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))

        event = TemperatureEvent(event_details=message)
        event_dispatcher.dispatch(event_name=EventDispatcher.TEMPERATURE_SAVE, event=event)

    def get_humidity(self, mqtt_client, event_dispatcher, mqtt_details):
        pending_measurement = True
        humidity = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                humidity = self._sensor.data.humidity
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "humidity": humidity
        }

        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))

    def get_pressure(self, mqtt_client, event_dispatcher, mqtt_details):
        pending_measurement = True
        pressure = None

        while pending_measurement:
            if self._sensor.get_sensor_data():
                pressure = self._sensor.data.pressure
                pending_measurement = False
            time.sleep(0.5)

        # TODO formalise this into object
        message = {
            "pressure": pressure
        }

        mqtt_client.publish(mqtt_details['topic'], json.dumps(message))
