from src.Sensor import Sensor
from time import sleep
from bluepy.btle import Peripheral, BTLEException


class SensorTagCC2650(Sensor):

    def __init__(self, logger, device, device_address):
        """

        :param logger:
        :param Peripheral device:
        :param device_address:
        """
        Sensor.__init__(self, device, device_address)
        self._logger = logger

    def connect(self):
        self._logger.debug('Connecting to SensorTagCC2650')
        self._device.connect(self._device_address)

    def disconnect(self):
        self._logger.debug('Disconnecting from SensorTagCC2650')
        self._device.disconnect()

    def get_ambient_temperature(self):
        self._logger.debug('Getting ambient temperature')
        config = self._device.getCharacteristics(uuid='f000aa02-0451-4000-b000-000000000000')[0]
        data = self._device.getCharacteristics(uuid='f000aa01-0451-4000-b000-000000000000')[0]

        # TODO do something with response
        config.write(b'\x01', withResponse=True)

        raw_temp = data.read().hex()
        while raw_temp == '00000000':
            self._logger.debug('Raw temperature data is invalid, sleeping')
            sleep(1)
            raw_temp = data.read().hex()

        lsb = raw_temp[4:6]
        msb = raw_temp[6:]

        temperature = ((int(msb, 16) * 256 + int(lsb, 16)) / 4) * 0.03125

        # TODO do something with response
        config.write(b'\x00', withResponse=True)

        return temperature

    def get_humidity(self):
        self._logger.debug('Getting relative humidity')
        config = self._device.getCharacteristics(uuid='f000aa22-0451-4000-b000-000000000000')[0]
        data = self._device.getCharacteristics(uuid='f000aa21-0451-4000-b000-000000000000')[0]

        config.write(b'\x01', withResponse=True)

        raw_humidity = data.read().hex()
        while raw_humidity == '00000000':
            self._logger.debug('Raw humidity data is invalid, sleeping')
            sleep(1)
            raw_humidity = data.read().hex()

        lsb = raw_humidity[4:6]
        msb = raw_humidity[6:]

        humidity = ((int(msb, 16) * 256 + int(lsb, 16)) / 65536) * 100

        config.write(b'\x00', withResponse=True)

        return humidity

    def get_barometric_pressure(self):
        pass