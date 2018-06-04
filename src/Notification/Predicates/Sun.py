import datetime
import logging
import os

from sunrise_sunset.sunrise_sunset import SunriseSunset


class Sun:
    def __init__(self):
        self._latitude = float(os.getenv('LOCATION_LATITUDE'))
        self._longitude = float(os.getenv('LOCATION_LONGITUDE'))
        logging.info('Initialising Sun predicate with lat: {}, lon: {}'.format(self._latitude, self._longitude))

    def is_after_sunrise(self):
        now = datetime.datetime.utcnow()
        sunrise, sunset = self._calculate_sunrise_sunset(time=now)

        return now > sunrise

    def is_before_sunrise(self):
        now = datetime.datetime.utcnow()
        sunrise, sunset = self._calculate_sunrise_sunset(time=now)

        return now < sunrise

    def is_after_sunset(self):
        now = datetime.datetime.utcnow()
        sunrise, sunset = self._calculate_sunrise_sunset(time=now)

        return now > sunset

    def _calculate_sunrise_sunset(self, time):
        sun = SunriseSunset(
            time,
            latitude=self._latitude,
            longitude=self._longitude
        )
        return sun.calculate()
