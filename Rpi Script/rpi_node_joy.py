#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class Rpi(object):
    def __init__(self):
        rospy.loginfo("Starting Raspberry Pi node...")

        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_AV", Twist, queue_size = 1)
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_cb)           #future update, add teleop_twist_joy on roslaunch instead of joy_node pack

    def joy_cb(self, joy_msg, intuitive = False):
        vel = Twist()

        joy_val_drive = joy_msg.axes[1]
        joy_val_turn = joy_msg.axes[3]
        rbButton = joy_msg.buttons[5]

        duty = int(joy_val_drive * 30)
        servo = int(joy_val_turn * 2)

        vel.linear.x = duty
        vel.angular.z = servo

        if (rbButton > 0):              #will only publish if rbbutton is enabled
             self.cmd_vel_pub.publish(vel)


if __name__ == "__main__":
    rospy.init_node("Rpi_node", anonymous = False)
    rpi_node = Rpi()
    rospy.spin()
