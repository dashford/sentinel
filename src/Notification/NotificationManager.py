import datetime
import pytz
from astral import Astral


class NotificationManager:

    def __init__(self, configuration):
        self._allows = configuration['allow']
        self._denies = configuration['deny']

        self._astral = Astral()
        self._astral.solar_depression = 'civil'
        self._city = self._astral['Dublin']

    def is_satisfied(self):
        pass

    def _is_after_sunrise(self):
        now = pytz.timezone('Europe/Dublin').localize(datetime.datetime.now())
        sun = self._city.sun(local=True)
        return now > sun['sunrise']

    def _is_after_sunset(self):
        now = pytz.timezone('Europe/Dublin').localize(datetime.datetime.now())
        sun = self._city.sun(local=True)
        return now > sun['sunset']
