class EventDispatcher:

    TEMPERATURE_SAVED = 'temperature.saved'
    HUMIDITY_SAVED = 'humidity.saved'
    PRESSURE_SAVED = 'pressure.saved'
    AIR_QUALITY_SAVED = 'air_quality.saved'

    def __init__(self):
        self._subscribers = []

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def dispatch(self, event_name, event):
        for subscriber in self._subscribers:
            if event_name in subscriber.get_subscribed_events():
                subscriber.notify(event=event)
