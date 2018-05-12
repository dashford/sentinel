import time

from src.Event.EventDispatcher import EventDispatcher
from src.Event.Subscriber.Subscriber import Subscriber
from src.Notifications.LED.LED import LED


class TemperatureSubscriber(Subscriber):
    def __init__(self):
        pass

    def get_subscribed_events(self):
        return [
            EventDispatcher.TEMPERATURE_SAVED
        ]

    def notify(self, event):
        self._signal_led(event=event)

    def _signal_led(self, event):
        print('_signal_led called. event received: {}'.format(event.get_event()))
        led = LED()
        led.on(channel=23)
        time.sleep(2)
        led.off(channel=23)
