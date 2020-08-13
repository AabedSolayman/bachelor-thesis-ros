#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    
def listener():
    rospy.init_node('controller', anonymous=False)

    rospy.Subscriber("/robot_tf", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
	listener()
    except rospy.ROSInterruptException:
        pass
