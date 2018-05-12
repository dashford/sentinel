import RPi.GPIO as GPIO


class RGB:
    def __init__(self, configuration):
        self._R = configuration['channels'][0]['r']
        self._G = configuration['channels'][0]['g']
        self._B = configuration['channels'][0]['b']
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
