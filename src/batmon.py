#!/usr/bin/env python

# This code will control the battery test station

import rospy
from std_msgs.msg import UInt8
from batmon.msg import bat_data

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    rospy.init_node('batmonctl', anonymous=True)

    rospy.Subscriber("BATMON", bat_data, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
