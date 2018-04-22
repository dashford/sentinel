import os
import time

import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv, find_dotenv

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Subscriber.TemperatureSubscriber import TemperatureSubscriber
from src.MQTT.Factory import Factory
from src.Sensors.Factory import Factory as Device_Factory
from src.Values.Credentials import Credentials

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    with open('config.yaml') as fp:
        configuration = yaml.load(fp)

    event_dispatcher = EventDispatcher()

    temperature_subscriber = TemperatureSubscriber()

    event_dispatcher.add_subscriber(subscriber=temperature_subscriber)

    mqtt_credentials = Credentials(username=os.getenv('MQTT_USERNAME'), password=os.getenv('MQTT_PASSWORD'))
    mqtt_client = Factory.create_client(provider='paho', credentials=mqtt_credentials)
    mqtt_client.connect(host='192.168.1.12', port=1883)

    scheduler = BackgroundScheduler()

    for sensor in configuration['sensors']:
        device = Device_Factory.create_sensor(device=sensor['type'])
        for metric in sensor['metrics']:
            if metric['metric'] == 'temperature':
                scheduler.add_job(
                    device.get_temperature,
                    'interval',
                    seconds=metric['poll'],
                    args=[mqtt_client, event_dispatcher, metric['mqtt']]
                )
            elif metric['metric'] == 'humidity':
                scheduler.add_job(
                    device.get_humidity,
                    'interval',
                    seconds=metric['poll'],
                    args=[mqtt_client, event_dispatcher, metric['mqtt']]
                )
            elif metric['metric'] == 'pressure':
                scheduler.add_job(
                    device.get_pressure,
                    'interval',
                    seconds=metric['poll'],
                    args=[mqtt_client, event_dispatcher, metric['mqtt']]
                )

    mqtt_client.loop_start()
    scheduler.start()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        mqtt_client.loop_stop()
