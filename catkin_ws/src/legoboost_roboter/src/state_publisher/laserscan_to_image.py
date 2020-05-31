#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:09:30 2020

@author: Aabed Solayman
@description: This 

"""

import numpy as np
import cv2
import rospy
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image

from cv_bridge import CvBridge

    
class RangesImageConverter:
    """
    This class is a converter which converts LasecScan.ranges into Images using
    CvBrdige
    It has a subscriber and a publisher, which are connected to the same node
    The Subscriber gets the ranges from topic /scan 
    The Publisher publisher the images to topic /converted_images
       
    """
    laser_position = None
    room_coordinates = None
    ranges_arr_length = None
    room_diagonal = None
    angle_steps = None
    
    rate = None         #Publish rate
    bridge = None       #cvBridge instance
    pub = None          # Publisher
    

                                    
                                    
    def __init__(self,laser_position, room_coordinates, ranges_arr_length):
        #initializing variables
        self.laser_position = laser_position
        self.room_coordinates =  room_coordinates
        self.ranges_arr_length = ranges_arr_length
        self.room_diagonal = np.sqrt(room_coordinates[0]**2+room_coordinates[1]**2).astype(int)
        self.angles()
        self.bridge = CvBridge()
        
        #inizializing the converter node   
        rospy.init_node('ranges2image_converter', anonymous=True)
        
        #initialiting publisher
        self.pub = rospy.Publisher('converted_images', Image, queue_size=10, latch=True)

        #subscribe from scan and publish to converter_images
        rospy.Subscriber("/scan", LaserScan, self.ranges_callback)
        
        rospy.spin()

    # ranges_callback: Get the new ranges list and updates the image with this list.
    def ranges_callback(self,laser_data):
        rangesarr = np.asarray(laser_data.ranges)
        self.update_image(rangesarr)
        

    # images_publisher: Converts numpy array to image using CvBridgePublish
    #                   and then publish the image to the topic converted_images
    def images_publisher(self, image):
        image2msg = self.bridge.cv2_to_imgmsg(image, encoding="passthrough")      
        self.pub.publish(image2msg)        
        self.rate = rospy.Rate(100)
        
        
        
    # update_image: Updating the image with ranges_arrays
    def update_image(self,ranges_arr):    
        
        # Get infinity values and delete them
        inf_indexes= np.where(ranges_arr == np.inf)         
        ranges_array=np.delete(ranges_arr,inf_indexes[0])
        angle_steps = np.delete(self.angle_steps,inf_indexes[0])
        
        # Calculate each pixel position relative to the sensor position.
        # As Pixels are integer values, position must be changed to integers.
        # The resolution of the pixel is 100.
        # Example: An x distance of 0.58420347204 meter = pixel(58)
        # Greater Resolution = Bigger images = longer computing time, the idea is 
        # to minimalize the computing time as possible, while maintaing the
        # stability of the measurments.
        
        x = ranges_array*np.cos(angle_steps)
        y = ranges_array*np.sin(angle_steps)
        
        x_pixels = (x*100).astype(int) + self.laser_position[0]+self.room_coordinates[0]
        y_pixels = (y*100).astype(int) + self.laser_position[1]+self.room_coordinates[1]
    
        
        # Create a black image with enough space for the sensor to be at any place
        # in the room
        
        blank_image = np.zeros((self.room_diagonal+self.room_coordinates[0],
                                self.room_diagonal+self.room_coordinates[1], 3), np.uint8)
        
        foo = blank_image
        print("foo: {}".format(foo))  
     
       #Update the image pixels and publish the new image
        try:
            for i in range(0,np.size(ranges_array)):
                blank_image[x_pixels[i],y_pixels[i]] = (0, 0, 250)   
                cv2.imshow("Laser Scan", blank_image)
                self.images_publisher(blank_image)

            cv2.waitKey(1)
            
       
        except IndexError as error:
            rospy.loginfo("Error while scanning data. Make sure the scanner is set properly" 
                         " or make sure room coordinates are right")       
           
# Calculate angle steps and add them to angle_steps array  
    def angles(self):
        angles =[]
        angles.append(0)
        for i in range(1,self.ranges_arr_length):
            angles.append(angles[i-1]+(360/self.ranges_arr_length))
                
        self.angle_steps = np.deg2rad(angles)

            

if __name__ == '__main__':
    
    c1 = RangesImageConverter(laser_position = [16,9], room_coordinates =[50,75], ranges_arr_length = 500)











