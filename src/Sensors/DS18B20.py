# from w1thermsensor import W1ThermSensor

from src.Sensors.Sensor import Sensor


class DS18B20:

    unit_conversions = {
        # Sensor.UNIT_CELSIUS: W1ThermSensor.DEGREES_C
    }

    def __init__(self, id):
        self._id = id

    def get_temperature(self, unit=Sensor.UNIT_CELSIUS):
        pass
        # sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, self._id)
        # return sensor.get_temperature(unit=self.unit_conversions[unit])
