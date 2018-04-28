from abc import ABC, abstractmethod


class Subscriber(ABC):

    @abstractmethod
    def get_subscribed_events(self):
        pass

    @abstractmethod
    def notify(self, event):
        pass
