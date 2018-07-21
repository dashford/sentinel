import logging

from ds18b20 import DS18B20 as Sensor
from src.MQTT.Message.Message import Message
from src.MQTT.Message.Formatters.JsonFormatter import JsonFormatter


class DS18B20:

    def __init__(self, address):
        self._sensor = Sensor(sensor_id=address)

    def get_temperature(self, mqtt_client, event_dispatcher, metric_details):
        logging.debug('Initialising BME680 sensor')
        temperature = self._sensor.get_temperature()

        message = Message()
        message_formatter = JsonFormatter()
        message.add_key_value(key='temperature', value=temperature)
        message.add_key_value(key='success', value=True)

        logging.info('Publishing message for DS18B20 _get_temperature to MQTT broker')
        mqtt_client.publish(metric_details['mqtt']['topic'], message_formatter.format(message=message.get_message()))


