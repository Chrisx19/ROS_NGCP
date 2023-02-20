#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class Joystick(object):
    def __init__(self):
        rospy.loginfo("Starting joystick for turtle")

        self.cmd_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=10)

    def joy_cb(self, joy_msg):
        self.vel = Twist()

        self.vel.linear.x = 2 * joy_msg.axes[1]
        self.vel.angular.z = 3 * joy_msg.axes[3]
        self.cmd_pub.publish(self.vel)

if __name__ == "__main__":
    rospy.init_node("Turtle_Joy_Node", anonymous=False)
    joy = Joystick()
    rospy.spin()
