import os

from src.MQTT.Providers.Paho import Paho


class Factory:

    @staticmethod
    def create_client(provider, credentials):
        if provider == 'paho':
            return Paho(client_id=os.getenv('MQTT_CLIENT_ID'), credentials=credentials)
