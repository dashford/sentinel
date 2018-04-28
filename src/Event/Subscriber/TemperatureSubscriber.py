from src.Event.EventDispatcher import EventDispatcher


class TemperatureSubscriber:
    def __init__(self):
        pass

    def get_subscribed_events(self):
        return [
            EventDispatcher.TEMPERATURE_SAVE
        ]

    def notify(self, event):
        self._signal_led(event=event)

    def _signal_led(self, event):
        print('_signal_led called. event received: {}'.format(event.get_event()))
