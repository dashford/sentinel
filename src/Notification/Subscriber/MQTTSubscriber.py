from abc import ABC, abstractmethod


class MQTTSubscriber(ABC):

    @abstractmethod
    def notify(self, mosq, obj, msg):
        pass
