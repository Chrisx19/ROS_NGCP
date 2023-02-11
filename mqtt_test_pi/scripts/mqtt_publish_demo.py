# MQTT Publish Demo
# Publish two messages, to two different topics

from time import sleep
import paho.mqtt.publish as publish

#publish.single("CoreElectronics/test", "Hello", hostname="test.mosquitto.org")
#publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")
while True:
    publish("test_topic", "Testing", hostname="test.mosquitto.org")
    print("Published Test")
    sleep(1)