import time
from twisted.internet import task
from twisted.internet import reactor
from dotenv import load_dotenv, find_dotenv
import os
from src.MQTT.Factory import Factory
from src.Values.Credentials import Credentials


load_dotenv(find_dotenv())

mqtt_credentials = Credentials(username=os.getenv('MQTT_USERNAME'), password=os.getenv('MQTT_PASSWORD'))
mqtt_client = Factory.create_client(provider='paho', credentials=mqtt_credentials)
mqtt_client.connect(host='192.168.1.12', port=1883)


























# mqtt_client = mqtt.Client(client_id="atlas")
# mqtt_client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
# mqtt_client.connect(host='192.168.1.12', port=1883)