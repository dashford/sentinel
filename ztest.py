import time
from twisted.internet import task
from twisted.internet import reactor
import paho.mqtt.client as mqtt
from dotenv import load_dotenv, find_dotenv
import os

from src.Sensors.DS18B20 import DS18B20


def getTemp(mqtt_client):
    """
    Called at ever loop interval.
    """
    print('Publishing temperature')
    # sensor = DS18B20(id='021583ad40ff')
    # mqtt_client.publish(topic='test/sensor1', payload='{"temperature": %.2f}' % 37)
    return

    # if _loopCounter < loopTimes:
    #     _loopCounter += 1
    #     print('A new second has passed.')
    #     return

    # if failInTheEnd:
    #     raise Exception('Failure during loop execution.')

    # We looped enough times.
    # loop.stop()
    # return


def getTempTest():
    time.sleep(10)
    print('In getTempTest')
    return


def cbLoopDone(result):
    """
    Called when loop was stopped with success.
    """
    print("Loop done.")
    reactor.stop()


def ebLoopFailed(failure):
    """
    Called when loop execution failed.
    """
    print(failure.getBriefTraceback())
    reactor.stop()


# set up MQTT client on script init
# add function for getting sensor readings
load_dotenv(find_dotenv())
mqtt_client = mqtt.Client(client_id="atlas")
mqtt_client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
mqtt_client.connect(host='192.168.1.12', port=1883)

loop = task.LoopingCall(getTemp, (mqtt_client))
loopTest = task.LoopingCall(getTempTest)

# Start looping every 5 seconds.
loopDeferred = loop.start(5.0)
loopDeferredTest = loopTest.start(5.0)

# Add callbacks for stop and failure.
loopDeferred.addCallback(cbLoopDone)
loopDeferred.addErrback(ebLoopFailed)

reactor.run()
