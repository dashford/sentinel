from src.Sensors.BME280 import BME280
from src.Sensors.BME680 import BME680
from src.Sensors.DS18B20 import DS18B20
from src.Notification.Subscriber.LED.RGB import RGB


class Factory:

    @staticmethod
    def create_sensor(device, address):
        if device == 'BME280':
            return BME280()
        elif device == 'BME680':
            return BME680(address=address)
        elif device == 'DS18B20':
            return DS18B20(address=address)

    @staticmethod
    def create_led(device, configuration, notification_manager):
        if device == 'rgb':
            return RGB(configuration=configuration, notification_manager=notification_manager)
