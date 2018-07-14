# from Adafruit_BME280 import BME280 as Device
# from Adafruit_BME280.BME280 import BME280_OSAMPLE_8
#from twisted.internet import defer

from src.Sensors.Sensor import Sensor


class BME280:
    def __init__(self):
        self._sensor = None
        # self._sensor = Device(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    async def get_temperature(self, unit=Sensor.UNIT_CELSIUS):
        """
        Return measured temperature from the device.

        :param string unit:
        :return float:
        """
        print('get_temperature')
        # d = defer.Deferred()
        # d.addCallback(self._some_other())
        # return defer.succeed(self._some_other())
        return 10.0
        if unit == Sensor.UNIT_CELSIUS:
            return self._sensor.read_temperature()

    def _some_other(self):
        return 11

    def get_humidity(self):
        """
        Return measured humidity from the device.

        :return float:
        """
        print('get_humidity')
        return 15.0
        return self._sensor.read_humidity()

    def get_pressure(self):
        """
        Return measured pressure from the device.

        :return float:
        """
        print('get_pressure')
        return 27.1
        return self._sensor.read_pressure()
