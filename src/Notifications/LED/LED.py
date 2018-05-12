import RPi.GPIO as GPIO


class LED:
    def __init__(self):
        # TODO: testing only
        #       Multiple LEDs will be connected to one pi so will need to take
        #       these values from config.
        r = 23
        g = 24
        b = 25
        pins = [r, g, b]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

    def on(self, channel):
        GPIO.output(channel, GPIO.HIGH)

    def off(self, channel):
        GPIO.output(channel, GPIO.LOW)
