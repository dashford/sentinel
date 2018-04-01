from src.MQTT.Factory import Factory


class MQTT:
    def __init__(self):
        self._client = None

    def _get_client(self):
        self._client = Factory.create_client()
        pass

    def publish(self, topic, payload):
        pass