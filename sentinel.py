import os
import time

import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv, find_dotenv

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Subscriber.TemperatureSubscriber import TemperatureSubscriber
from src.Event.Subscriber.HumiditySubscriber import HumiditySubscriber
from src.Event.Subscriber.PressureSubscriber import PressureSubscriber
from src.Event.Subscriber.AirQualitySubscriber import AirQualitySubscriber
from src.MQTT.Factory import Factory
from src.Sensors.Factory import Factory as Device_Factory
from src.Values.Credentials import Credentials
from src.Notification.NotificationManager import NotificationManager

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    with open('config.yaml') as fp:
        configuration = yaml.load(fp)

    event_dispatcher = EventDispatcher()
    event_dispatcher.add_subscriber(subscriber=TemperatureSubscriber())
    event_dispatcher.add_subscriber(subscriber=HumiditySubscriber())
    event_dispatcher.add_subscriber(subscriber=PressureSubscriber())
    event_dispatcher.add_subscriber(subscriber=AirQualitySubscriber())

    mqtt_credentials = Credentials(username=os.getenv('MQTT_USERNAME'), password=os.getenv('MQTT_PASSWORD'))
    mqtt_client = Factory.create_client(provider=os.getenv('MQTT_PROVIDER'), credentials=mqtt_credentials)
    mqtt_client.connect(host=os.getenv('MQTT_HOST'), port=int(os.getenv('MQTT_PORT')))

    for led in configuration['leds']:
        led_device = Device_Factory.create_led(
            device=led['type'],
            configuration=led,
            notification_manager=NotificationManager(configuration=led['notifications'])
        )
        for topic in led['mqtt']['topics']:
            mqtt_client.message_callback_add(subscription=topic['topic'], callback=led_device.notify)

    # mqtt_client.subscribe(topic='brompton/living-room/#')

    scheduler = BackgroundScheduler()

    for sensor in configuration['sensors']:
        device = Device_Factory.create_sensor(device=sensor['type'])
        # TODO come up with better way to add these jobs
        for metric in sensor['metrics']:
            if metric['metric'] == 'temperature':
                scheduler.add_job(
                    device.get_temperature,
                    'interval',
                    seconds=metric['poll'],
                    args=[mqtt_client, event_dispatcher, metric]
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
            elif metric['metric'] == 'air_quality':
                scheduler.add_job(
                    device.get_air_quality,
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
