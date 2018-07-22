from src.Notification.Predicates.Sun import Sun


class NotificationManager:

    def __init__(self, configuration):
        self._allows = configuration['allow']
        self._denies = configuration['deny']
        self._sun_predicate = Sun()

    def is_satisfied(self):
        for denied in self._denies:
            if denied == 'after_sunset' and self._sun_predicate.is_after_sunset():
                return False
            if denied == 'after_sunrise' and self._sun_predicate.is_after_sunrise():
                return False
            if denied == 'all':
                return False

        for allowed in self._allows:
            if allowed == 'after_sunset' and self._sun_predicate.is_after_sunset():
                return True
            if allowed == 'after_sunrise' and self._sun_predicate.is_after_sunrise():
                return True

        return False
