# class Countdown(object):
#     counter = 5
#
#     def count(self):
#         if self.counter == 0:
#             reactor.stop()
#         else:
#             print(self.counter, '...')
#             self.counter -= 1
#             reactor.callLater(1, self.count)
#
#
# def hello():
#     print('Hello from the reactor loop!')
#     print('Lately I feel like I\'m stuck in a rut.')
#
#
# from twisted.internet import reactor
#
# reactor.callWhenRunning(Countdown().count)
# reactor.callWhenRunning(hello)
#
# print('Start!')
# reactor.run()
# print('Stop!')


# from twisted.internet.task import react
# import treq
#
# def get_url(urls):
#
#     def handle_response(resp):
#         print("Got response code %d from %s" % (resp.code, site))
#
#     def handle_failure(failure):
#         print("Something failed: %s" % failure.getErrorMessage())
#
#     for site in urls:
#         print("Getting URL %s" % site)
#         d = treq.get(site)
#         d.addCallback(handle_response)
#         d.addErrback(handle_failure)
#
#     return d
#
# def main(reactor, *args):
#     urls = ['http://google.com', 'http://gmail.com']
#     d = get_url(urls)
#     return d
#
# react(main)


from bluetooth import *

# Create the client socket
client_socket = BluetoothSocket(RFCOMM)

client_socket.connect(("54:6C:0E:79:3C:85", 3))

client_socket.send("Hello World")

print("Finished")

client_socket.close()






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