from src.MQTT.Providers.Paho import Paho


class Factory:

    @staticmethod
    def create_client(provider, client_id, credentials):
        if provider == 'paho':
            return Paho(client_id=client_id, credentials=credentials)
