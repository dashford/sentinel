from bluepy import btle
from time import sleep
import logging
import requests
import datetime
from src.Sensors.SensorTagCC2650 import SensorTagCC2650
from bluepy.btle import BTLEException
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

logger = logging.getLogger('SentinelClient')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
stdout_channel = logging.StreamHandler()
stdout_channel.setLevel(logging.DEBUG)
stdout_channel.setFormatter(formatter)
logger.addHandler(stdout_channel)

# TODO use device factory or pass device factory into Sensor directly
# device = btle.Peripheral(None)
# TODO use address factory e.g. MACAddress object?
# device_address = '54:6C:0E:79:3C:85'

# sensor = SensorTagCC2650(logger, device, device_address)
# sensor.connect()

mqtt_client = mqtt.Client(client_id="atlas")
mqtt_client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
mqtt_client.connect(host='192.168.1.12', port=1883)

while True:
    submission_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "021583ad40ff")
    print("Sensor 1 has temperature %.2f" % sensor.get_temperature())
    mqtt_client.publish(topic='test/sensor1', payload='{"temperature": %.2f}' % sensor.get_temperature())

    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "021583a99eff")
    print("Sensor 2 has temperature %.2f" % sensor.get_temperature())
    mqtt_client.publish(topic='test/sensor2', payload='{"temperature": %.2f}' % sensor.get_temperature())
    # for sensor in W1ThermSensor.get_available_sensors():
    #     print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
    # try:
    #     temperature = sensor.get_ambient_temperature()
    #     humidity = sensor.get_humidity()
    # except BTLEException as e:
    #     # TODO Make exception more generic
    #     logger.debug('Sensor has lost connection, trying to re-connect')
    #     sensor.connect()
    #
    # logger.info(
    #     'Temperature: {temperature}; Humidity: {humidity}; Submission Time: {submission}'.format(
    #         temperature=temperature, humidity=humidity, submission=submission_time
    #     )
    # )
    # payload = {
    #     'sensor_id': '3560747b-e756-49f9-939e-27bfa4199173',
    #     'temperature': temperature,
    #     'submitted_at': submission_time
    # }
    # r = requests.post("http://192.168.1.12:3001/temperatures", data=payload)
    # logger.info(r.text)
    # payload = {
    #     'sensor_id': '3560747b-e756-49f9-939e-27bfa4199173',
    #     'humidity': humidity,
    #     'submitted_at': submission_time
    # }
    # r = requests.post("http://192.168.1.12:3001/humidities", data=payload)
    # logger.info(r.text)
    print('sleeping')
    sleep(30)
