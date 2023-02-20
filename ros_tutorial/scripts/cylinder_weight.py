#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from ros_tutorial.msg import Cylinder

volume = 0      #Global Variable_volume
density = 0     #Global Variable_density

density_found = False
volume_found = False

def density_callback(data):
    global density
    global density_found
    density = data.data
    density_found = True

def cy_callback(cy_msg):
    global volume
    global volume_found
    volume = cy_msg.volume
    volume_found = True

def weight_calc():
    if volume_found and density_found:
        weight = volume * density
        pub_weight.publish(weight)

rospy.init_node("cylinder_weight")
pub_weight = rospy.Publisher("/weight", Float64, queue_size=10)
sub_Cylinder_msg = rospy.Subscriber("/cylinder", Cylinder, cy_callback)	#Call back is like a reference but instead of data this will be msg data
sub_density = rospy.Subscriber("/density", Float64, density_callback)       #Sub to density value

while not rospy.is_shutdown():
    weight_calc()
    rospy.sleep(0.1)
