#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import controller_constants
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import rospy
from turtlesim.msg import Pose


distance_control_lst = []
x_lst = []
y_lst = []
theta_lst =[]
left_wheel_speed_lst = []
right_wheel_speed_lst = []
dt_lst = []


pose_from_sensor = [0,0,0]


# This method is the implementation of drivline algorithm in "Robotics, vision 
# and Control by Peter Corke" It gets a line of ax+by+c=0, the initial pose and 
# returns the actual pose x,y,theta. It also calculates the left wheel speed,
# right wheel speed by using the angular and linear velocities

def following_line(pose, factors):
    
    x = pose[0]
    y = pose[1]
    theta = pose[2]
    
    
    K_d = 0.5
    K_h = 1
    
    slope = math.atan2(-factors[0],factors[1])
    
    angle_difference = K_h*(slope -  theta)

    #iteration and plotting purposes
    x_lst.append(x)
    y_lst.append(y)
    theta_lst.append(theta)       
    
    #Speed controller: calculcate the distnce from line to control speed
    distance_control = K_d* distance_from_line(x,y,factors)
    distance_control_lst.append(distance_control)
    
    #Heading controller: calculate the angle difference between slope and theta
    angle_difference = K_h*(slope -  theta)
    
    #omega is equivalent to the steering wheel angle
    omega = angle_difference - distance_control
    
#       # TODO: Check if omega exceeds the maximum angular velocity
#        if(omega>2):
#            omega = 2
#        elif(omega<2):
#            omega = -2
    
    #sending velocities to the left and rigtht wheels
    wheels_velocity_control(omega)
    
    
#This method is for calculating the distance from the robot to the line. 
#Input: actual positions of the robot and factors [a,b,c] of the line ax+by+c=0
#Output: distance 
        
def distance_from_line(x,y,factors):
    
    return (x*factors[0] +y*factors[1] + factors[2])/math.sqrt(factors[0]**2 + factors[1]**2)




def wheels_velocity_control(angular_velocity):
    
    #TODO: Change velocities to PWM signals and publish them
    
    linear_velocity = controller_constants.LINEAR_VELOCITY
    wheel_radius = controller_constants.WHEEL_RADIUS
    wheel_width = controller_constants.WHEEL_WIDTH
    
    left_wheel_speed = (linear_velocity- wheel_width*angular_velocity)/wheel_radius
    right_wheel_speed = (linear_velocity+ wheel_width*angular_velocity)/wheel_radius
   
    right_wheel_speed_lst.append(right_wheel_speed)
    left_wheel_speed_lst.append(left_wheel_speed)
    
    

def pose_callback(pose_msg):
    
    global pose_from_sensor
    pose_from_sensor = [pose_msg.x,
            pose_msg.y,
            pose_msg.theta]
    
    
def sub_pose():
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
    
if __name__ == '__main__':
    
    try:
        i = 0
        while(i<100):
            i+=0.001
            dt_lst.append(i)
            
            #TODO: Subscribe to Pose message  (which is sent by the sensor)

            following_line(pose_from_sensor,factors=[1,1,-1])
        
       
        
        
        
        #plots:
        plt.plot(dt_lst, distance_control_lst)
        plt.grid(True)
        plt.title("Distance to line ")
        plt.xlabel('time')
        plt.ylabel('distance to line')
        plt.show()
        
        
        plt.plot(x_lst, y_lst)
        plt.grid(True)
        plt.title("Robot Motion")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


        x = np.linspace(-5,5,100)
        y=-x + 1
        
        plt.plot(x, y, '-r', label='y=-x+1')
        plt.grid(True)
        plt.title("Line to be followed y=-x+1")        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

        plt.plot(x_lst,y_lst,x,y)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
    finally:
        print("END")
        
