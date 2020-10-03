from src.Devices.Sensors.BME280 import BME280
from src.Devices.Sensors.BME680 import BME680
from src.Devices.Sensors.CCS811 import CCS811
from src.Devices.Sensors.DS18B20 import DS18B20
from src.Devices.Sensors.LTR559 import LTR559
from src.Devices.Sensors.PMS5003 import PMS5003


class Factory:

    @staticmethod
    def create_sensor(device, address):
        if device == 'BME280':
            return BME280(address=address)
        elif device == 'BME680':
            return BME680(address=address)
        elif device == 'DS18B20':
            return DS18B20(address=address)
        elif device == 'CCS811':
            return CCS811(address=address)
        elif device == 'LTR559':
            return LTR559(address=address)
        elif device == 'PMS5003':
            return PMS5003(address=address)
