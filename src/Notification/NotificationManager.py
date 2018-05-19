import datetime
import os

import pytz

from sunrise_sunset.sunrise_sunset import SunriseSunset


class NotificationManager:

    def __init__(self, configuration):
        self._allows = configuration['allow']
        self._denies = configuration['deny']

        self._latitude = float(os.getenv('LOCATION_LATITUDE'))
        self._longitude = float(os.getenv('LOCATION_LONGITUDE'))

    def is_satisfied(self):
        pass

    def _is_after_sunrise(self):
        sun = SunriseSunset(
            pytz.timezone('Europe/Dublin').localize(datetime.datetime.now()),
            latitude=self._latitude,
            longitude=self._longitude
        )
        # sun = self._city.sun(local=True)
        # return now > sun['sunrise']

    def _is_after_sunset(self):
        now = pytz.timezone('Europe/Dublin').localize(datetime.datetime.now())
        # sun = self._city.sun(local=True)
        # return now > sun['sunset']
