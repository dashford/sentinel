from src.Sensors.BME280 import BME280
from src.Sensors.BME680 import BME680


class Factory:

    @staticmethod
    def create_sensor(device):
        if device == 'BME280':
            return BME280()
        elif device == 'BME680':
            return BME680()
