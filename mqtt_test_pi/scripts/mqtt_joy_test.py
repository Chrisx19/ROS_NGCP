#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy

# Subscribe to Joy node, send Joy value to other Pi
# via MQTT, will transform into rostopic for STM
from time import sleep
import paho.mqtt.publish as publish

def joy_cb(joy_msg):
    if joy_msg.axes[1] != 0:
        linear_x = joy_msg.axes[1] * 100
    else:
        linear_x = 0

    publish.single("joy_test_topic", linear_x, hostname="test.mosquitto.org")
    print("Published Test")

joy_sub = rospy.Subscriber("/joy", Joy, joy_cb, queue_size = 1)

if __name__ == "__main__":
    rospy.init_node("mqtt_joy_test", anonymous=False)
    rospy.spin()