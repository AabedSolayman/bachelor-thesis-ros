#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
import controller_constants
import matplotlib.pyplot as plt
import numpy as np
import rospy
from geometry_msgs.msg import TransformStamped
from tf.transformations import euler_from_quaternion
from pylgbst import*
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK
from pylgbst.comms.cgatt import GattConnection

# =============================================================================
#  This script is the implementation of drivline algorithm in "Robotics, vision 
#  and Control by Peter Corke" It gets a line of ax+by+c=0, the pose and calculates
#  the left wheel speed, right wheel speed of the robot.
# =============================================================================
     


distance_control_lst = []
x_lst = []
y_lst = []
theta_lst =[]
left_wheel_speed_lst = []
right_wheel_speed_lst = []
dt_lst = []
linear_velocity = 0


#Callback function: to be called every time the subscriber gets a new pose message
# Parameters: (robotTF): this is the topic which includes the pose of the robot
def pose_callback(robotTF):
    #factors ax+by+c=0, a=1, b=1, c=0 
    factors=[1,0,0.5]
    
    #INPUTS
    x = robotTF.transform.translation.x
    y = robotTF.transform.translation.y
    q_z = robotTF.transform.rotation.z
    q_w = robotTF.transform.rotation.w

    print("x = {}".format(x))
    print("y = {}".format(y))

    euler = euler_from_quaternion([0,0,q_z,q_w])
    theta = euler[2]
    
    K_d = 0.5
    K_h = 1.8
    
    #CONTROLLER CALCULATION
        #Distance: calculcate the distnce from line to control speed
    distance_control = K_d*  (x*factors[0] +y*factors[1] + factors[2])/math.sqrt(factors[0]**2 + factors[1]**2)
    
    #Steering Angle: calculate the angle difference between slope and theta
    slope = np.arctan2(-factors[0],factors[1])
    angle_difference = (slope -  theta)
    #angle_difference = (angle_difference+np.pi) % (2*np.pi) - np.pi #between -pi to pi
    omega = K_h*angle_difference - distance_control

    

    #WHEEL VELOCITIES
    global linear_velocity

    wheel_radius = controller_constants.WHEEL_RADIUS
    wheel_width = controller_constants.WHEEL_WIDTH
    left_wheel_speed = 0.0008*(1 - wheel_width*omega)/wheel_radius
    right_wheel_speed = 0.0008*(1 + wheel_width*omega)/wheel_radius
       
    #Robot velocities must be a value between 0 and 1
    if (left_wheel_speed>1):left_wheel_speed = 1
    if (right_wheel_speed>1):right_wheel_speed = 1
    
    if (left_wheel_speed<0):left_wheel_speed = 0
    if (right_wheel_speed<0):right_wheel_speed = 0
	

 
   #Send velocities to the robot
    hub.motor_AB.start_speed(speed_primary=right_wheel_speed,speed_secondary=left_wheel_speed)
    
    #print("Angle Difference = {}".format(angle_difference))
    #print("Distance Control = {}".format(distance_control))
    #print("WheelWidth*Omega = {}".format(omega*wheel_width))
        
    
    #Adding values into lists for plotting purposes
    x_lst.append(x)
    y_lst.append(y)
    theta_lst.append(angle_difference)       
    distance_control_lst.append(distance_control)
    right_wheel_speed_lst.append(right_wheel_speed)
    left_wheel_speed_lst.append(left_wheel_speed)
    

def sub_pose():
    rospy.init_node('controller',anonymous=True) 
    rospy.Subscriber('/robot_tf', TransformStamped, pose_callback)    
    rospy.spin()   
    
    


    
if __name__ == '__main__':

         
    try:

      
        HUB_MAC = '00:16:53:A8:E1:8D' # MAC-Adresse des MoveHubs
        conn = GattConnection("hci0")
        conn.connect(HUB_MAC)  # you can pass Hub mac address as parameter here, like 'AA:BB:CC:DD:EE:FF'
        hub = MoveHub(conn)

        if(hub!= None):
            print("Connected")
            sub_pose()

        else:
            print("Connection error")


         
	#Plot
	font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
		
	plt.rc('font', **font)
        plot4 = plt.figure(1)
        plt.plot(x_lst,y_lst,linewidth=4)
	#plt.axhline(y=0.5,linewidth=4,color='r')
        plt.grid(True)
        plt.title("Actual Path/ Desired Path")
        plt.xlabel('x')
        plt.ylabel('y')

    finally:

        hub.disconnect()
        print("END.... Disconnected")

        plt.show()
