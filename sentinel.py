from bluepy import btle
from time import sleep
import logging
import requests
from src.Sensors.SensorTagCC2650 import SensorTagCC2650

logger = logging.getLogger('SentinelClient')
logger.setLevel(logging.DEBUG)

# TODO use device factory or pass device factory into Sensor directly
device = btle.Peripheral(None)
# TODO use address factory e.g. MACAddress object?
device_address = '54:6C:0E:79:3C:85'

sensor = SensorTagCC2650(logger, device, device_address)
sensor.connect()

for n in range(0, 10):
    temperature = sensor.get_ambient_temperature()
    humidity = sensor.get_humidity()
    print(
        'Temperature: {temperature}; Humidity: {humidity}'.format(
            temperature=temperature, humidity=humidity
        )
    )
    payload = {'sensor_id': 1, 'temperature': temperature}
    r = requests.post("http://localhost:3001/temperatures", data=payload)
    print(r.text)
    payload = {'sensor_id': 1, 'humidity': humidity}
    r = requests.post("http://localhost:3001/humidities", data=payload)
    print(r.text)
    sleep(5)

sensor.disconnect()
