class TemperatureEvent:
    def __init__(self, event_details):
        self._event_details = event_details

    def get_event(self):
        return self._event_details
