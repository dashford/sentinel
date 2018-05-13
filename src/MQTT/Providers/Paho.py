import paho.mqtt.client as paho
import logging


class Paho:
    def __init__(self, client_id, credentials=None):
        self._client = paho.Client(client_id=client_id)
        if credentials:
            self._client.username_pw_set(credentials.get_username(), credentials.get_password())
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish = self._on_publish
        self._client.on_subscribe = self._on_subscribe

    def connect(self, host, port=1883, keepalive=60, bind_address=""):
        logging.info('Connecting to broker on {}:{}'.format(host, port))
        self._client.connect(host=host, port=port, keepalive=keepalive, bind_address=bind_address)

    def publish(self, topic, payload=None, qos=0, retain=False):
        logging.info('Publishing message to topic {}'.format(topic))
        self._client.publish(topic=topic, payload=payload, qos=qos, retain=retain)

    def subscribe(self, topic, qos=0):
        logging.info('Subscribing to topic {}'.format(topic))
        self._client.subscribe(topic=topic, qos=qos)

    def message_callback_add(self, subscription, callback):
        logging.info('Adding callback for subscription {}'.format(subscription))
        self._client.message_callback_add(sub=subscription, callback=callback)

    def loop_start(self):
        self._client.loop_start()

    def loop_stop(self):
        self._client.loop_stop()

    def _on_connect(self, client, userdata, flags, rc):
        logging.info('Connected with result code {}'.format(rc))

    def _on_disconnect(self, client, userdata, rc):
        if rc != paho.MQTT_ERR_SUCCESS:
            logging.error('Disconnect was unexpected')
            pass
        logging.info('Disconnected from broker')

    def _on_publish(self, client, userdata, mid):
        logging.info('Message with ID {} published'.format(mid))

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print('_on_subscribe called')
