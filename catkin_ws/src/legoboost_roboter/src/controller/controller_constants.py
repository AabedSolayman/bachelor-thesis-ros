# -*- coding: utf-8 -*-

WHEEL_WIDTH = 0.064

WHEEL_RADIUS = 0.0152

# This method is the Unicycle implementation. It calculates the actual pose of the
# robot using equations 4.2 and 4.7 from Robotics Vision and control by Peter Corke
# Input: linear velocity, angular velocity, steering wheel angle theta
#def unicycle(linear_velocity,angular_velocity,theta):
#    
#    dt= 1/100          # Time 
#    a = 1e-2            # Offset to the next frame or next position
#    x = (math.cos(theta)*linear_velocity - a*math.sin(theta)*angular_velocity)*dt
#    y = (math.sin(theta)*linear_velocity + a*math.cos(theta)*angular_velocity)*dt
#    theta = angular_velocity*dt
#    
#    return x,y,theta
#    
