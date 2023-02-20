#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from ros_tutorial.msg import Cylinder	#Taking the MSG file I created called Cylinder.msg 
#^Custom data structure

from math import pi			#Used for math (pi = 3.14)

radius = 0		#initializing radius global variable
radius_squared = 0	#initializing radius global variable
height = 0		#initializing radius global variable

radius_found = False		#radius found is false so that the value dont get used until found is true 
radius_squared_found = False	#False so it doesnt get used until true 
height_found = False

def radius_callback(data):		#This func is only called if radius is received
	global radius			#Since radius is global
	global radius_found
	radius = data.data		#Taking the data from the publisher /radius
	radius_found = True		#If radius is found, then use this call back to another func

def radius_squared_callback(data):
        global radius_squared
        global radius_squared_found
        radius_squared = data.data	#Taking the data from the publisher /radius_squared
        radius_squared_found = True

def height_callback(data):
        global height
        global height_found
        height = data.data		#Taking the data from the publisher /height
        height_found = True

def calculate():
	if radius_found and radius_squared_found and height_found:		#If all of them are true then continue to this function
		msg_cy = Cylinder()						#This is the msg file created, gonna use this as parameter init
		msg_cy.volume = pi * radius_squared *height			#Inside of msg file created made, volume
		msg_cy.surface_area = 2 * pi * (radius * height + radius_squared)#Inside of msg file created made, surface_area
		pub_cy.publish(msg_cy)						#publish the value on topic "Cylinder"

rospy.init_node("cylinder_calc")					#Always start the script with title for node
rospy.Subscriber("/radius", Float64, radius_callback)			#Subscribe to radius topic to get data, and making a call back for callback function
rospy.Subscriber("/radius_squared", Float64, radius_squared_callback)
rospy.Subscriber("/height", Float64, height_callback)
pub_cy = rospy.Publisher("/cylinder", Cylinder, queue_size=10)		#Published the cylinder calculated as topic 


while not rospy.is_shutdown():
	calculate()	#So that it calculate all the time but this is going to calculate if all variable is found
	rospy.sleep(0.1)
