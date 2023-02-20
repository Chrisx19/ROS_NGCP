#!/usr/bin/env python3
import rospy
import time
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 

x = 5.5444445610046
y = 5.5444445610046
theta = 0

def pos_callback(pose_msg):     #grabbing data on msg file
    global x, y, theta        #making a variable file for x, y theta
    x = pose_msg.x              #data from msg file on x
    y = pose_msg.y
    theta = pose_msg.theta
    
def goal_turn():
    vel = Twist()
    global x, y, theta
    
    kp_turn = 4.8   #Proportional error for feedback
    rospy.loginfo("Moving to coordinate (%.2f, %.2f).", goal_x, goal_y)

    start_time = time.time()
    while (time.time() - start_time) < 1:   #one second to turn
        goal = math.atan2 ((goal_y - y), (goal_x - y) )
        
        vel.linear.x = 0.0                          #m/s
        vel.angular.z = (goal - theta) * kp_turn   #rad/sec     Distance = (Goal - postion)
        vel_pub.publish(vel)
        time.sleep(0.1)
    vel.angular.z = 0.0                       
    vel_pub.publish(vel)

def goal_distance():
    vel = Twist()
    global x, y

    kp_distance = 0.859

    start_time = time.time()
    while (time.time() - start_time) < 1:   #going forward
        rospy.loginfo("Current Position (%.2f, %.2f).", x, y)
        distance = math.sqrt( pow(goal_x - x, 2) + pow(goal_y - y, 2) )
        
        vel.linear.x = distance * kp_distance             #m/s
        vel.angular.z = 0.0     #rad/sec
        vel_pub.publish(vel)
        time.sleep(0.1)
    vel.angular.z = 0.0                       
    vel_pub.publish(vel)
    time.sleep(1)
    rospy.loginfo("Target has reached (%.2f, %.2f).", x, y)
    
rospy.init_node('turtle')
vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
pose_sub = rospy.Subscriber('turtle1/pose', Pose, pos_callback)

x_goal = rospy.get_param("x", 5.5444445610046)
x_curr = rospy.set_param('x', x_goal)

y_goal = rospy.get_param("y", 5.5444445610046)
y_curr = rospy.set_param('y', y_goal)

goal_x = x_goal
goal_y = y_goal
goal_turn()
goal_distance()


