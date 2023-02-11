#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test_topic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    mqtt_ros_pub.publish(str(msg.payload))

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("test.mosquitto.org", 1883, 60)

rospy.init_node("mqtt_subscriber", anonymous=False)
mqtt_ros_pub = rospy.Publisher("/mqttData", String, queue_size=10)

client.loop_forever()
rospy.spin()