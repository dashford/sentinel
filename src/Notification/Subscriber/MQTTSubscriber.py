from abc import ABC, abstractmethod


class MQTTSubscriber(ABC):

    @abstractmethod
    def notify(self, mosq, obj, msg):
        pass
        # add is_statisfied_by constraints here to prevent notification proceeding (require inspection of msg?)
        # as this method will be implemented by more than LEDs in theory
