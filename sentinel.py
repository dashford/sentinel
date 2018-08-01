import logging
import os
import sys
import time

import RPi.GPIO as GPIO
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv, find_dotenv
from blinker import signal

from src.MQTT.Factory import Factory
from src.Notification.NotificationManager import NotificationManager
from src.Sensors.Factory import Factory as Device_Factory
from src.Values.Credentials import Credentials
from src.Signals.Subscribers.MQTT import MQTT as MQTTSubscriber

if __name__ == '__main__':
    # TODO decide on format
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
    logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.DEBUG)

    load_dotenv(find_dotenv())
    with open('config.yaml') as fp:
        configuration = yaml.load(fp)

    mqtt_client = Factory.create_client(
        provider=os.getenv('MQTT_PROVIDER'),
        credentials=Credentials(username=os.getenv('MQTT_USERNAME'), password=os.getenv('MQTT_PASSWORD'))
    )
    mqtt_client.connect(host=os.getenv('MQTT_HOST'), port=int(os.getenv('MQTT_PORT')))

    mqtt_signal_subscriber = MQTTSubscriber(mqtt_client=mqtt_client)

    temperature_signal = signal('temperature')
    humidity_signal = signal('humidity')
    pressure_signal = signal('pressure')
    air_quality_signal = signal('air_quality')

    temperature_signal.connect(mqtt_signal_subscriber.notify)
    humidity_signal.connect(mqtt_signal_subscriber.notify)
    pressure_signal.connect(mqtt_signal_subscriber.notify)
    air_quality_signal.connect(mqtt_signal_subscriber.notify)

    if 'leds' in configuration:
        leds = {}
        for index, led in enumerate(configuration['leds']):
            leds[index] = Device_Factory.create_led(
                device=led['type'],
                configuration=led,
                notification_manager=NotificationManager(configuration=led['notifications'])
            )
            for topic in led['mqtt']['topics']:
                mqtt_client.message_callback_add(subscription=topic['topic'], callback=leds[index].notify)

    mqtt_client.subscribe(topic='brompton/#')

    scheduler = BackgroundScheduler()

    for sensor in configuration['sensors']:
        device = Device_Factory.create_sensor(device=sensor['type'], address=sensor['address'])
        # TODO come up with better way to add these jobs
        for metric in sensor['metrics']:
            if metric['metric'] == 'temperature':
                scheduler.add_job(
                    device.get_temperature,
                    'interval',
                    seconds=metric['poll'],
                    args=[metric['mqtt']]
                )
            elif metric['metric'] == 'humidity':
                scheduler.add_job(
                    device.get_humidity,
                    'interval',
                    seconds=metric['poll'],
                    args=[metric['mqtt']]
                )
            elif metric['metric'] == 'pressure':
                scheduler.add_job(
                    device.get_pressure,
                    'interval',
                    seconds=metric['poll'],
                    args=[metric['mqtt']]
                )
            elif metric['metric'] == 'air_quality':
                scheduler.add_job(
                    device.get_air_quality,
                    'interval',
                    seconds=metric['poll'],
                    args=[metric['mqtt']]
                )

    mqtt_client.loop_start()
    scheduler.start()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        mqtt_client.loop_stop()
    finally:
        GPIO.cleanup()
