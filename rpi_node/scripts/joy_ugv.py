#!/usr/bin/env python3
import rospy
from rpi_node.msg import CmdVelUgv
from sensor_msgs.msg import Joy

class Joystick(object):
    def __init__(self):
        rospy.loginfo("Starting joystick for turtle")

        self.cmd_pub = rospy.Publisher("/rpi_ugv_info", CmdVelUgv, queue_size=10)
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=10)

    def joy_cb(self, joy_msg):
        vel = CmdVelUgv()

        pwm = 2 * joy_msg.axes[1]
        servo = 3 * joy_msg.axes[3]
        en_button = joy_msg.buttons[5]

        vel.Linear_x_PWM = int(pwm)
        vel.Angular_z_Servo = int(servo)

        if(en_button>0): 
            self.cmd_pub.publish(vel)

    # def MTi_cb(self, mti):

if __name__ == "__main__":
    rospy.init_node("ugv_joy", anonymous=False)
    joy = Joystick()
    rospy.spin()