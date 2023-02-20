#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

def callback(data): 			#Call back function from Subs
	radius = data.data		#Extract the data
	squared_radius = radius * radius     #Does the math
	pub.publish(squared_radius)	#Publish out the value

rospy.init_node("radius_squarer")
pub = rospy.Publisher("/radius_squared", Float64, queue_size=10)
rospy.Subscriber("/radius", Float64, callback)	#Call back is like a reference 
rospy.spin() #Infinite loop that keeps the program alive
