import time

import RPi.GPIO as GPIO


class RGB:
    def __init__(self, configuration):
        self._id = configuration['id']
        self._R = configuration['channels']['r']
        self._G = configuration['channels']['g']
        self._B = configuration['channels']['b']
        pins = [
            self._R,
            self._G,
            self._B
        ]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

    def blink(self, mosq, obj, msg):
        print(msg.payload)
        led = GPIO.PWM(self._G, 100)
        led.start(0)
        for i in range(0, 100):
            led.ChangeDutyCycle(i)
            time.sleep(0.02)
        led.stop()


        # GPIO.output(self._G, GPIO.HIGH)
        # time.sleep(2)
        # GPIO.output(self._G, GPIO.LOW)

    # def red(self):
    #     return self._R
    #
    # def green(self):
    #     return self._G
    #
    # def blue(self):
    #     return self._B
    #
    # def on(self, channel):
    #     GPIO.output(channel, GPIO.HIGH)
    #
    # def off(self, channel):
    #     GPIO.output(channel, GPIO.LOW)
