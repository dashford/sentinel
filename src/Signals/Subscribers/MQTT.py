import logging
from src.MQTT.Message.Message import Message
from src.MQTT.Message.Formatters.JsonFormatter import JsonFormatter


class MQTT:
    def __init__(self, mqtt_client):
        logging.debug('Initialising MQTT signal subscriber')
        self._mqtt_client = mqtt_client

    def notify(self, sender=None, **kwargs):
        message = Message()
        message_formatter = JsonFormatter()

        for key, value in kwargs.items():
            message.add_key_value(key=key, value=value)

        logging.debug('MQTT message: {}'.format(message.get_message()))

        self._mqtt_client.publish(kwargs['mqtt_topic'], message_formatter.format(message=message.get_message()))
