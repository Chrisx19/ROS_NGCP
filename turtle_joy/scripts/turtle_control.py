#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def pose_callback(data):
  cmd = Twist()
  cmd.linear.x = data.axes[1]
  cmd.angular.z = data.axes[3]
  pub.publish(cmd)

if __name__ == '__main__':
  rospy.init_node("control")
  pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
  sub = rospy.Subscriber("/joy", Joy, callback=pose_callback)
  rospy.loginfo("Node has been started.")

  rospy.spin()

