import logging

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Subscriber.Subscriber import Subscriber


class TemperatureSubscriber(Subscriber):
    def __init__(self):
        pass

    def get_subscribed_events(self):
        # TODO: will need to assign methods to particular events for finer control
        return [
            EventDispatcher.TEMPERATURE_SAVED
        ]

    def notify(self, event):
        self._signal_led(event=event)

    def _signal_led(self, event):
        logging.debug('_signal_led called')
