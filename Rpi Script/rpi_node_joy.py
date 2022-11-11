#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class Rpi(object):
    def __init__(self):
        rospy.loginfo("Starting Raspberry Pi node...")

        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_ugv", Twist, queue_size = 10)
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=10)

    def joy_cb(self, joy_msg):
        self.vel = Twist()

        joy_val_drive = joy_msg.axes[1]
        joy_val_turn = joy_msg.axes[3]

        duty = joy_val_drive * 100
        servo = joy_val_turn * 50

        self.vel.linear.x = duty
        self.vel.angular.z = servo

        self.cmd_vel_pub.publish(self.vel)

if __name__ == "__main__":
    rospy.init_node("Rpi_node", anonymous = False)
    rpi_n = Rpi()
    rospy.spin()
