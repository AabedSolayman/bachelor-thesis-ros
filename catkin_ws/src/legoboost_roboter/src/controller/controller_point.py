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


distance_control_lst = []
x_lst = []
y_lst = []
theta_lst =[]
left_wheel_speed_lst = []
right_wheel_speed_lst = []
dt_lst = []
linear_velocity = 0



def pose_callback(robotTF):
    following_line(robotTF,factors=[-1,1,0.25])
    

def sub_pose():
    rospy.init_node('controller',anonymous=True)
    rospy.Subscriber('/robot_tf', TransformStamped, pose_callback)    
    rospy.spin()   
    
    
    
    
    
    
    
# This method is the implementation of drivline algorithm in "Robotics, vision 
# and Control by Peter Corke" It gets a line of ax+by+c=0, the pose It also 
# calculates the left wheel speed, right wheel speed by using the angular 
# and linear velocities

def following_line(pose, factors):
    
    #INPUTS
    x = pose.transform.translation.x
    y = pose.transform.translation.y
    q_z = pose.transform.rotation.z
    q_w = pose.transform.rotation.w
    
    euler = euler_from_quaternion([0,0,q_z,q_w])
    theta = euler[2]
    print("theta: {}".format(theta*180/np.pi))
    K_d = 0.2
    K_h = 0.1
    
    #CONTROLLER CALCULATION
        #Distance: calculcate the distnce from line to control speed
    distance_control = K_d* distance_from_line(x,y,factors) 
    
        #Steering Angle: calculate the angle difference between slope and theta
    slope = math.atan2(-factors[0],factors[1])
    angle_difference = K_h*(slope -  theta)
    omega = angle_difference - distance_control
    
    
    #WHEEL VELOCITIES
    wheels_velocity(omega) 

    #iteration and plotting purposes
    x_lst.append(x)
    y_lst.append(y)
    theta_lst.append(theta)       
    distance_control_lst.append(distance_control)

    
#This method is for calculating the distance from the robot to the line. 
#Input: actual positions of the robot and factors [a,b,c] of the line ax+by+c=0
#Output: distance 
        
def distance_from_line(x,y,factors):
    
    return (x*factors[0] +y*factors[1] + factors[2])/math.sqrt(factors[0]**2 + factors[1]**2)




def wheels_velocity(angular_velocity):
    
    #TODO: Change velocities to PWM signals and publish them
    global linear_velocity
  #  print("linear_velocity = {}".format(linear_velocity))
    
    wheel_radius = controller_constants.WHEEL_RADIUS
    wheel_width = controller_constants.WHEEL_WIDTH
    left_wheel_speed = 0.012*(linear_velocity- wheel_width*angular_velocity)/wheel_radius
    right_wheel_speed = 0.012*(linear_velocity+ wheel_width*angular_velocity)/wheel_radius
    
    if (left_wheel_speed>1 or left_wheel_speed<-1):left_wheel_speed/abs(left_wheel_speed)
    if (right_wheel_speed>1 or right_wheel_speed<-1):right_wheel_speed/abs(right_wheel_speed)

    linear_velocity = 0.5*(left_wheel_speed+left_wheel_speed)
    
    right_wheel_speed_lst.append(right_wheel_speed)
    left_wheel_speed_lst.append(left_wheel_speed)
    hub.motor_AB.start_speed(speed_primary=right_wheel_speed,speed_secondary=left_wheel_speed)
            
   # print("speed_right = {}".format(right_wheel_speed))
   # print("speed_left = {}".format(left_wheel_speed))
    
    
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

        #PLOTS:
        plot1 = plt.figure(1)
        plt.plot(x_lst, y_lst)
        plt.grid(True)
        plt.title("Robot Motion")
        plt.xlabel('x')
        plt.ylabel('y')


        x = np.linspace(-5,5,100)
        y=-x
        
        plot2 = plt.figure(2)
        plt.plot(x, y, '-r', label='y=-x+1')
        plt.grid(True)
        plt.title("Line to be followed y=-x+1")        
        plt.xlabel('x')
        plt.ylabel('y')


        plot3 = plt.figure(3)
        plt.plot(distance_control_lst)
        plt.grid(True)
        plt.title("Distance to line ")
        plt.xlabel('time')
        plt.ylabel('distance to line')

         
        plot4 = plt.figure(4)
        plt.plot(x_lst,y_lst,x,y)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.show()

        
    finally:
        hub.disconnect()
        print("END.... Disconnected")

        
