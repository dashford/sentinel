import RPi.GPIO as GPIO


class RGB:
    def __init__(self, configuration):
        print(configuration)
        # TODO: don't use indices here
        self._R = configuration['channels'][0]
        self._G = configuration['channels'][1]
        self._B = configuration['channels'][2]
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
