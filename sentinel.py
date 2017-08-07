from bluepy import btle
from time import sleep
import logging
import requests
import datetime
from src.Sensors.SensorTagCC2650 import SensorTagCC2650

logger = logging.getLogger('SentinelClient')
logger.setLevel(logging.DEBUG)

# TODO use device factory or pass device factory into Sensor directly
device = btle.Peripheral(None)
# TODO use address factory e.g. MACAddress object?
device_address = '54:6C:0E:79:3C:85'

sensor = SensorTagCC2650(logger, device, device_address)
sensor.connect()

while True:
#for n in range(0, 10):
    submission_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    temperature = sensor.get_ambient_temperature()
    humidity = sensor.get_humidity()
    print(
        'Temperature: {temperature}; Humidity: {humidity}; Submission Time: {submission}'.format(
            temperature=temperature, humidity=humidity, submission=submission_time
        )
    )
    payload = {
        'sensor_id': '3560747b-e756-49f9-939e-27bfa4199173',
        'temperature': temperature,
        'submitted_at': submission_time
    }
    r = requests.post("http://192.168.1.12:3001/temperatures", data=payload)
    print(r.text)
    payload = {
        'sensor_id': '3560747b-e756-49f9-939e-27bfa4199173',
        'humidity': humidity,
        'submitted_at': submission_time
    }
    r = requests.post("http://192.168.1.12:3001/humidities", data=payload)
    print(r.text)
    sleep(30)

sensor.disconnect()
