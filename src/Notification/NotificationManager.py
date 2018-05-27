import datetime
import os

from sunrise_sunset.sunrise_sunset import SunriseSunset


class NotificationManager:

    def __init__(self, configuration):
        self._allows = configuration['allow']
        self._denies = configuration['deny']

        self._latitude = float(os.getenv('LOCATION_LATITUDE'))
        self._longitude = float(os.getenv('LOCATION_LONGITUDE'))

    def is_satisfied(self):
        for denied in self._denies:
            if denied == 'after_sunset' and self._is_after_sunset():
                return False
            if denied == 'after_sunrise' and self._is_after_sunrise():
                return False
            if denied == 'all':
                return False

        for allowed in self._allows:
            if allowed == 'after_sunset' and self._is_after_sunset():
                return True
            if allowed == 'after_sunrise' and self._is_after_sunrise():
                return True

        return False

    def _is_after_sunrise(self):
        now = datetime.datetime.utcnow()
        sun = SunriseSunset(
            now,
            latitude=self._latitude,
            longitude=self._longitude
        )
        sunrise, sunset = sun.calculate()

        return now > sunrise

    def _is_after_sunset(self):
        now = datetime.datetime.utcnow()
        sun = SunriseSunset(
            now,
            latitude=self._latitude,
            longitude=self._longitude
        )
        sunrise, sunset = sun.calculate()

        return now > sunset
