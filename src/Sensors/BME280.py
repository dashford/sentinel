from Adafruit_BME280 import BME280 as sensor
from Adafruit_BME280.BME280 import BME280_OSAMPLE_8


class BME280:
    def __init__(self):
        self._sensor = sensor(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def get_temperature(self):
        return self._sensor.read_temperature()

    def get_humidity(self):
        return self._sensor.read_humidity()

    def get_pressure(self):
        return self._sensor.read_pressure()