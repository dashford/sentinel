import logging
import os
import sys
import time

import RPi.GPIO as GPIO
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv, find_dotenv
from blinker import signal

from src.MQTT.Factory import Factory as MQTTFactory
from src.Devices.Sensors.Factory import Factory as Sensor_Factory
from src.Values.Credentials import Credentials
from src.Signals.Subscribers.MQTT import MQTT as MQTTSignalSubscriber


def _initialise_logging():
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
    logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.DEBUG)
    return logging.getLogger('sentinel')


def _load_env():
    load_dotenv(find_dotenv())


def _load_configuration():
    with open('config.yaml') as file:
        return yaml.load(file)


if __name__ == '__main__':
    logger = _initialise_logging()
    _load_env()
    configuration = _load_configuration()

    mqtt_client = MQTTFactory.create_client(
        provider=os.getenv('MQTT_PROVIDER'),
        client_id=os.getenv('MQTT_CLIENT_ID'),
        credentials=Credentials(
            username=os.getenv('MQTT_USERNAME'),
            password=os.getenv('MQTT_PASSWORD')
        )
    )
    mqtt_client.connect(host=os.getenv('MQTT_HOST'), port=os.getenv('MQTT_PORT'))

    scheduler = BackgroundScheduler()

    broadcasts = []
    signal_subscribers = []

    for sensor in configuration['sensors']:
        device = Sensor_Factory.create_sensor(device=sensor['type'], address=sensor['address'])
        for metric in sensor['metrics']:
            mqtt_signal_subscriber = MQTTSignalSubscriber(
                logger=logger,
                mqtt_client=mqtt_client,
                publish_topic=metric['mqtt']['topic']
            )

            broadcast = signal(metric['metric'])
            broadcast.connect(mqtt_signal_subscriber.notify, sender=device)

            signal_subscribers.append(mqtt_signal_subscriber)
            broadcasts.append(broadcast)

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
            elif metric['metric'] == 'lux':
                scheduler.add_job(
                    device.get_lux,
                    'interval',
                    seconds=metric['poll'],
                    args=[metric['mqtt']]
                )
            elif metric['metric'] == 'particulate_matter':
                scheduler.add_job(
                    device.get_particulate_matter,
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


# TODO:
# use click library for CLI interaction
# fix logging name
# pass logging level as ENV parameter
# marshmallow to validate configuration