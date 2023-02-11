#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from turtlesim.srv import TeleportRelative
from std_srvs.srv import Empty
from math import pi

def call_tpRelative_service(linear, angular):
    try:
        tp_relative = rospy.ServiceProxy("/turtle1/teleport_relative",TeleportRelative)
        tp_Res = tp_relative(linear, angular)
        rospy.loginfo(tp_Res)
    except rospy.ServiceException as e:
        rospy.warn(e)

def call_reset_service():
    try:
        reset = rospy.ServiceProxy("/reset",Empty)
        reset_Res = reset()
        rospy.loginfo(reset_Res)
    except rospy.ServiceException as f:
        rospy.warn(f)

def joy_callback(joyData):
    vel = Twist()

    vel.linear.x = joyData.axes[1] * 3.0
    vel.angular.z = joyData.axes[3] * 3.0

    # teleports in direction of button
    aButton = joyData.buttons[0]
    bButton = joyData.buttons[1]
    xButton = joyData.buttons[2]
    yButton = joyData.buttons[3]

    # left bumper slows down, right bumper speeds up
    lbButton = joyData.buttons[4]
    rbButton = joyData.buttons[5]

    # right arrow resets
    rArrowButton = joyData.buttons[7]

    if(aButton>0): call_tpRelative_service(-5,0)
    if(bButton>0): call_tpRelative_service(5,pi/-2)
    if(xButton>0): call_tpRelative_service(5,pi/2)
    if(yButton>0): call_tpRelative_service(5,0)
    if(lbButton>0): vel.linear.x -= 2
    if(rbButton>0): vel.linear.x += 3
    if(rArrowButton>0): call_reset_service()

    velPub.publish(vel)

# Closed Loop System
if __name__ == '__main__':
    rospy.init_node("turtle_joy")
    velPub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    joySub = rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.loginfo("Turtle Joy Node has been started.")

    rospy.spin()
