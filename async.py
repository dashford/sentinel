# import time
# from twisted.internet import stdio, reactor, task, threads, endpoints, protocol, defer
# from twisted.internet.endpoints import StandardIOEndpoint
# from twisted.internet.protocol import connectionDone
# from twisted.protocols import basic
# from src.Sensors.SensorTagCC2650 import SensorTagCC2650
# from bluepy import btle
# import logging


# class WebCheckerCommandProtocol(basic.LineReceiver):
#     delimiter = b'\n'  # unix terminal style newlines. remove this line
#
#     def __init__(self):
#         self.sensor = ''
#         self.logger = ''
#
#     def connectionMade(self):
#         self.logger = logging.getLogger('Sentinel')
#         self.logger.setLevel(logging.DEBUG)
#         formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
#         stdout_channel = logging.StreamHandler()
#         stdout_channel.setLevel(logging.DEBUG)
#         stdout_channel.setFormatter(formatter)
#         self.logger.addHandler(stdout_channel)
#         device = btle.Peripheral(None)
#         device_address = '54:6C:0E:79:3C:85'
#         self.sensor = SensorTagCC2650(self.logger, device, device_address)
#         self.sensor.connect()
#         self.check()
#
#     def lineReceived(self, line):
#         pass
#
#     def quit(self):
#         """quit: Quit this session"""
#         self.sendLine(b'Goodbye.')
#         self.transport.loseConnection()
#
#     def check(self):
#         humidity = 0.0
#         d = threads.deferToThread(self.sensor.get_ambient_temperature())
#         # a = threads.deferToThread(self.sensor.get_humidity())
#         d.addCallback(self.david)
#         return d
#         # a.addCallback(self.david)
#         # temperature = self.sensor.get_ambient_temperature()
#         # self.logger.info('Temperature: {temperature}; Humidity: {humidity}'.format(
#         #     temperature=temperature, humidity=humidity
#         # ))
#         # self.quit()
#         # self.sendLine(b'Got temperature and humidity')
#
#     def david(self, temperature):
#         self.logger.info('Value: {temperature}'.format(
#             temperature=temperature
#         ))
#
#     def connectionLost(self, reason):
#         # stop the reactor, only because this is meant to be run in Stdio.
#         self.sensor.disconnect()
#         reactor.stop()


# class SensorProtocol(basic.LineReceiver):
#     def connectionMade(self):
#         self.factory.logger.info('Test from connectionMade')
#         # self.transport.write(b"Test from connectionMade\r\n")
#         self.lineReceived('test')
#
#     def lineReceived(self, line):
#         self.factory.logger.info('Test from lineReceived')
#         # self.transport.write(b"Test from lineReceived\r\n")
#         d = self.factory.getAmbientTemperature()
#
#         def onError(err):
#             return 'Internal error in server'
#         d.addErrback(onError)
#
#         def writeResponse(message):
#             self.transport.write(message + b'\r\n')
#             self.transport.loseConnection()
#         d.addCallback(writeResponse)
#
#     def connectionLost(self, reason=connectionDone):
#         self.factory.logger.info('Test from connectionLost')
#         # reactor.stop()
#
#
# class SensorFactory(protocol.ServerFactory):
#     protocol = SensorProtocol
#
#     def __init__(self, id):
#         self.id = id
#         self.logger = logging.getLogger('Sentinel')
#         self.logger.setLevel(logging.DEBUG)
#         formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
#         stdout_channel = logging.StreamHandler()
#         stdout_channel.setLevel(logging.DEBUG)
#         stdout_channel.setFormatter(formatter)
#         self.logger.addHandler(stdout_channel)
#         device = btle.Peripheral(None)
#         device_address = '54:6C:0E:79:3C:85'
#         self.logger.info('Test from __init__ {}'.format(self.id))
#         # self.sensor = SensorTagCC2650(self.logger, device, device_address)
#         # self.sensor.connect()
#
#     def getAmbientTemperature(self):
#         self.logger.info('called getAmbientTemperature from {}'.format(self.id))
#         return defer.succeed(b"Text from deferTest\r\n")
#
#
# if __name__ == "__main__":
#     endpoint = StandardIOEndpoint(reactor=reactor)
#     endpoint.listen(SensorFactory(id=1))
#     reactor.run()






# retrieve from API list of devices to poll
#   - this needs to get an updated list every minute
# for each device get the relevant values from the on board sensors
#   - e.g. one device could have temp and humidity.
#   - each sensor would be its own operation

# - API call would be its own class and method that registers callLater
#   The above class has a method get_devices() that's called to populate the loop
#   -- one detail: this method might not be up to date depending on where the API call
#      is taking place but should be mostly accurate.
# - API call should also return capabilities (e.g. temp, humidity, light) so the client
#   knows what sensors to ask for and how to get them.
# - Who controls the reactor loop? Ideally reactor only queries devices once every 30 seconds
#   but not sure how to control this?
#   Maybe a callLater too? Or whenever the API call returns a new list the reactor iterates
#   as fast as it can and waits until the next API call.

# endpoint persistent client connections
# - http://twistedmatrix.com/documents/current/core/howto/endpoints.html














from twisted.application.internet import ClientService, backoffPolicy
from twisted.internet import reactor, protocol, endpoints
import logging
from twisted.protocols import basic
from twisted.internet.protocol import connectionDone, Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import StandardIOEndpoint, ProcessEndpoint, TCP4ServerEndpoint


class BluetoothService(ClientService):
    def __init__(self, endpoint, factory):
        ClientService.__init__(self, endpoint, factory, retryPolicy=backoffPolicy(initialDelay=5.0))

    def startService(self):
        print('startService called')
        ClientService.startService(self)

    def stopService(self):
        print('stopService called')

    def whenConnected(self, failAfterFailures=None):
        print('whenConnected called')


class SensorProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        print('SensorProtocol __init__ called')
        # As mentioned above, this, along with auxiliary classes and functions,
        # is where most of the code is.

    def connectionMade(self):
        # The connectionMade event is usually where setup of the connection object
        # happens.
        print('Test from connectionMade')
        print('some_state is currently {}'.format(self.factory.some_state))
        self.factory.some_state = self.factory.some_state + 1
        # self.transport.loseConnection()

    def dataReceived(self, data):
        print('dataReceived called')

    def connectionLost(self, reason=connectionDone):
        # The connectionLost event is where tearing down of any connection-specific
        # objects is done.
        print('Test from connectionLost')
        # self.factory.some_state = self.factory.some_state - 1

    def getAmbientTemperature(self):
        print('called getAmbientTemperature')


class SensorFactory(protocol.Factory):
    some_state = 0

    # find way to populate these automatically
    mac_addresses = [
        '54:6C:0E:79:3C:85'
    ]

    def __init__(self):
        print('SensorFactory __init__ called')
        # The factory is used to share state that exists beyond the lifetime of any given connection
        # The persistent configuration is kept in a Factory class

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        # print('Resetting reconnection delay')
        # self.resetDelay()
        return SensorProtocol(self)

    def startFactory(self):
        print('startFactory called')

    def stopFactory(self):
        print('stopFactory called')



if __name__ == "__main__":
    # client
    # reactor.connectTCP('localhost', 8007, SensorFactory())
    # reactor.run()

    # server
    # endpoint = TCP4ServerEndpoint(reactor, 8007)
    # endpoint.listen(SensorFactory())
    # reactor.run()

    endpoint = ProcessEndpoint(reactor=reactor, executable=None)
    factory = SensorFactory()
    service = BluetoothService(endpoint, factory)
    service.startService()
    reactor.run()

# python async.py and curl localhost:8007
# run server for each sensor?
# run one client that queries servers periodically