import time

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Subscriber.Subscriber import Subscriber


class TemperatureSubscriber(Subscriber):
    def __init__(self, led):
        # TODO: refactor led to not be so specific, just for testing at the moment
        self._led = led

    def get_subscribed_events(self):
        # TODO: will need to assign methods to particular events for finer control
        return [
            EventDispatcher.TEMPERATURE_SAVED
        ]

    def notify(self, event):
        self._signal_led(event=event)

    def _signal_led(self, event):
        print('_signal_led called. event received: {}'.format(event.get_event()))
        self._led.on(channel=self._led.red())
        time.sleep(2)
        self._led.off(channel=self._led.red())
