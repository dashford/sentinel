import time

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
        self._red_gpio = configuration['channels']['r']
        self._green_gpio = configuration['channels']['g']
        self._blue_gpio = configuration['channels']['b']

        self._channels = {
            self.RED: self._red_gpio,
            self.GREEN: self._green_gpio,
            self.BLUE: self._blue_gpio
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

        self._initialise_gpio()

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
            raise NotImplementedError
            # self._pulse(channel=self._map_rgb_to_single_channel(rgb=rgb))
        elif style == 'flash':
            self._flash(rgb=self._map_rgb_to_percentages(rgb=rgb))

        time.sleep(0.5)

    def _initialise_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self._red_gpio, self._green_gpio, self._blue_gpio], GPIO.OUT, initial=GPIO.LOW)

        self._red = GPIO.PWM(self._red_gpio, 100)
        self._green = GPIO.PWM(self._green_gpio, 100)
        self._blue = GPIO.PWM(self._blue_gpio, 100)

        self._red.start(0)
        self._green.start(0)
        self._blue.start(0)

    def _flash(self, rgb, duration=0.1):
        self._red.ChangeDutyCycle(rgb['red'])
        self._green.ChangeDutyCycle(rgb['green'])
        self._blue.ChangeDutyCycle(rgb['blue'])

        time.sleep(duration)

        self._red.ChangeDutyCycle(0)
        self._green.ChangeDutyCycle(0)
        self._blue.ChangeDutyCycle(0)

    # def _pulse(self, channel, frequency=100, speed=0.005, step=1):
    #     self._initialise_gpio()
    #     p = GPIO.PWM(channel, frequency)
    #     p.start(0)
    #     for duty_cycle in range(0, 100, step):
    #         p.ChangeDutyCycle(duty_cycle)
    #         time.sleep(speed)
    #     for duty_cycle in range(100, 0, -step):
    #         p.ChangeDutyCycle(duty_cycle)
    #         time.sleep(speed)
    #     p.stop()
    #     self._clean_up()

    def _map_rgb_to_single_channel(self, rgb):
        for component in rgb:
            if rgb[component] == 255:
                return self._channels[component]

    def _map_rgb_to_percentages(self, rgb):
        return {x: (rgb[x] / 255.0) * 100 for x in rgb}
