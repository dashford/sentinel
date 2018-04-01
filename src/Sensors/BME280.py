from Adafruit_BME280 import BME280 as Device
from Adafruit_BME280.BME280 import BME280_OSAMPLE_8

from src.Sensors.Sensor import Sensor


class BME280:
    def __init__(self):
        self._sensor = Device(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def get_temperature(self, unit=Sensor.UNIT_CELSIUS):
        """
        Return measured temperature from the device.

        :param string unit:
        :return float:
        """
        if unit == Sensor.UNIT_CELSIUS:
            return self._sensor.read_temperature()

    def get_humidity(self):
        """
        Return measured humidity from the device.

        :return float:
        """
        return self._sensor.read_humidity()

    def get_pressure(self):
        """
        Return measured pressure from the device.

        :return float:
        """
        return self._sensor.read_pressure()
