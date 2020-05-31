#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python program to illustrate HoughLine 
# method for line detection 
import cv2 
import numpy as np 
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image


bridge = CvBridge()

def images_callback(image):
    try:
        img = bridge.imgmsg_to_cv2(image, "passthrough")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(gray, 1, np.pi/180, 10, minLineLength=10, maxLineGap=250)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
    
    
        cv2.imshow("Result Image", img)
    
        cv2.waitKey(1)
    #    cv2.destroyAllWindows()
    except CvBridgeError as e:
        print(e)

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("/converted_images", Image, images_callback)
rospy.spin()


  
## Read image 
#img = cv2.imread('LS3.png', cv2.IMREAD_COLOR) # road.png is the filename
## Convert the image to gray-scale
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
## Find the edges in the image using canny detector
##edges = cv2.Canny(gray, 50, 200)
## Detect points that form a line
#lines = cv2.HoughLinesP(gray, 1, np.pi/180, 10, minLineLength=10, maxLineGap=250)
## Draw lines on the image
#for line in lines:
#    x1, y1, x2, y2 = line[0]
#    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
## Show result
#cv2.imshow("Result Image", img)
#
#cv2.waitKey()
#cv2.destroyAllWindows()