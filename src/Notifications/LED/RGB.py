import RPi.GPIO as GPIO


class RGB:
    def __init__(self, configuration):
        # TODO: testing only
        #       Multiple LEDs will be connected to one pi so will need to take
        #       these values from config.
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

    def red(self):
        return self._R

    def green(self):
        return self._G

    def blue(self):
        return self._B

    def on(self, channel):
        GPIO.output(channel, GPIO.HIGH)

    def off(self, channel):
        GPIO.output(channel, GPIO.LOW)
