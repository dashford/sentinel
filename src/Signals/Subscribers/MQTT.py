from src.MQTT.Message.Message import Message
from src.MQTT.Message.Formatters.JsonFormatter import JsonFormatter


class MQTT:
    def __init__(self, logger, mqtt_client, publish_topic):
        self._mqtt_client = mqtt_client
        self._publish_topic = publish_topic
        self._logger = logger
        self._logger.debug('Initialising MQTT signal subscriber')

    def notify(self, sender=None, **kwargs):
        message = Message()
        message_formatter = JsonFormatter()

        for key, value in kwargs.items():
            message.add_key_value(key=key, value=value)

        self._mqtt_client.publish(self._publish_topic, message_formatter.format(message=message.get_message()))
