class BME680:
    def __init__(self):
        self._sensor = None

    def get_temperature(self, mqtt_client, event_dispatcher, mqtt_details):
        mqtt_client.publish(mqtt_details['topic'], 1)
        # call event_dispatcher
