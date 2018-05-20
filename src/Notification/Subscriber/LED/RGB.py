import time
import sys
import logging
log_format = '%(levelname)s | %(asctime)-15s | %(message)s'
logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.DEBUG)

import RPi.GPIO as GPIO
from src.Notification.Subscriber.MQTTSubscriber import MQTTSubscriber


class RGB(MQTTSubscriber):

    GREEN = 'green'
    RED = 'red'
    BLUE = 'blue'

    DEFAULT_COLOUR = GREEN
    DEFAULT_STYLE = 'flash'

    def __init__(self, configuration, notification_manager):
        self._notification_manager = notification_manager

        self._id = configuration['id']
        self._topics = configuration['mqtt']['topics']
        self._R = configuration['channels']['r']
        self._G = configuration['channels']['g']
        self._B = configuration['channels']['b']

        self._channels = {
            self.RED: self._R,
            self.GREEN: self._G,
            self.BLUE: self._B
        }

        self._rgb_colours = {
            self.RED: {
                'red': 255,
                'green': 0,
                'blue': 0
            },
            self.GREEN: {
                'red': 0,
                'green': 255,
                'blue': 0
            },
            self.BLUE: {
                'red': 0,
                'green': 0,
                'blue': 255
            }
        }

        self._valid_pulse_colours = [
            self._rgb_colours['red'],
            self._rgb_colours['green'],
            self._rgb_colours['blue']
        ]

    def notify(self, mosq, obj, msg):
        if self._notification_manager.is_satisfied() is False:
            raise Exception('NotificationManager not satisfied based on current conditions')

        rgb = self._rgb_colours[self.DEFAULT_COLOUR]
        style = self.DEFAULT_STYLE

        for topic in self._topics:
            if topic['topic'] == msg.topic and 'colour' in topic:
                rgb = {
                    'red': topic['colour']['red'],
                    'green': topic['colour']['green'],
                    'blue': topic['colour']['blue']
                }
            if topic['topic'] == msg.topic and 'style' in topic:
                style = topic['style']

        if style == 'pulse' and rgb not in self._valid_pulse_colours:
            raise Exception('colour must be one of {}'.format(self._valid_pulse_colours))

        if style == 'pulse':
            print('calling pulse')
            self._pulse(channel=self._map_rgb_to_single_channel(rgb=rgb))
        elif style == 'flash':
            print('calling flash')
            self._flash(rgb=self._map_rgb_to_percentages(rgb=rgb))

        time.sleep(0.5)

    def _initialise_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self._R, self._G, self._B], GPIO.OUT, initial=GPIO.LOW)

    def _clean_up(self):
        GPIO.cleanup()

    def _pulse(self, channel, frequency=100, speed=0.005, step=1):
        self._initialise_gpio()
        p = GPIO.PWM(channel, frequency)
        p.start(0)
        for duty_cycle in range(0, 100, step):
            p.ChangeDutyCycle(duty_cycle)
            time.sleep(speed)
        for duty_cycle in range(100, 0, -step):
            p.ChangeDutyCycle(duty_cycle)
            time.sleep(speed)
        p.stop()
        self._clean_up()

    def _flash(self, rgb, frequency=100, duration=0.1):
        try:
            self._initialise_gpio()
            print('_flash setting PWM')

            red = GPIO.PWM(self._R, frequency)
            green = GPIO.PWM(self._G, frequency)
            blue = GPIO.PWM(self._B, frequency)

            print('_flash start 0')
            red.start(0)
            green.start(0)
            blue.start(0)

            print('_flash changedutycycle')
            red.ChangeDutyCycle(rgb['red'])
            green.ChangeDutyCycle(rgb['green'])
            blue.ChangeDutyCycle(rgb['blue'])

            print('_flash sleep')
            time.sleep(duration)

            print('_flash stop')
            red.stop()
            green.stop()
            blue.stop()
        except Exception as e:
            print(e)
        finally:
            print('_flash clean up')
            self._clean_up()

    def _map_rgb_to_single_channel(self, rgb):
        for component in rgb:
            if rgb[component] == 255:
                return self._channels[component]

    def _map_rgb_to_percentages(self, rgb):
        return {x: (rgb[x] / 255.0) * 100 for x in rgb}
