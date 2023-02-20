#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class Joystick(object):
  def __init__(self):
    rospy.loginfo("Starting joystick for UGV")

    self.cmd_pub = rospy.Publisher("/cmd_vel_ugv", Twist, queue_size=10)
    self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_cb, queue_size=10)

  def joy_cb(self, joy_msg):
#    self.vel = Twist()
    self.ugv_vel_msg = Twist()
#    self.vel.linear.x = 2 * joy_msg.axes[1]
    self.ugv_vel_msg.linear.x = 2 * joy_msg.axes[1]
#    self.vel.angular.z = 3 * joy_msg.axes[3]
    self.ugv_vel_msg.angular.z = 3 * joy_msg.axes[3]

#    self.cmd_pub.publish(self.vel)
    self.cmd_pub.publish(self.ugv_vel_msg)

if __name__ == "__main__":
  rospy.init_node("UGV_joy_node", anonymous=False)
  joy = Joystick()
  rospy.spin()
