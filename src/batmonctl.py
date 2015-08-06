#!/usr/bin/env python

# This code will control the battery test station

import rospy
import time
from std_msgs.msg import UInt8
from batmon.msg import bat_data

#How many full charge- discharge cycles to do, even numbers ONLY!!!
Cycles = 2

val = None

def callback(data):
    global val
    val = data
    #rospy.loginfo(val)

# Charging discharging logic
    
def run():
    B1_st = Cycles*2
    B2_st = Cycles*2
    B3_st = Cycles*2
    B4_st = Cycles*2
    pub1 = rospy.Publisher('B1', UInt8, queue_size=1)
    pub2 = rospy.Publisher('B2', UInt8, queue_size=1)
    pub3 = rospy.Publisher('B3', UInt8, queue_size=1)
    pub4 = rospy.Publisher('B4', UInt8, queue_size=1)

    rospy.init_node('batmonctl', anonymous=True)

    rospy.Subscriber("BATMON", bat_data, callback)

    rate = rospy.Rate(1) # 1hz

    while val == None:
        rospy.loginfo("Waiting for first reading")
        time.sleep(0.5)

    time.sleep(5)

    #Check if battery present, Start charging
    if (val.Bat1_Volt > 5000):
        pub1.publish(1)
    else:
        B1_st = -1
        rospy.loginfo("Battery 1 not connected")
    if (val.Bat2_Volt > 5000):
        pub2.publish(1)
    else:
        B2_st = -1
        rospy.loginfo("Battery 2 not connected")
    if (val.Bat3_Volt > 5000):
        pub3.publish(1)
    else:
        B3_st = -1
        rospy.loginfo("Battery 3 not connected")
    if (val.Bat4_Volt > 5000):
        pub4.publish(1)
    else:
        B4_st = -1
        rospy.loginfo("Battery 4 not connected")
    
    time.sleep(5) # Time for first charge to take hold

    while not rospy.is_shutdown():
        if B1_st >0:
            if (B1_st % 2 == 0):
                if (val.Bat1_Curr <= 100): #charging is done
                    rospy.loginfo("Battery 1 Done Charging Cycle " + str(B1_st/2))
                    B1_st-=1
                    pub1.publish(2) #switch to discharge
            else:
                if(val.Bat1_Volt <= 10800): #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 1 Done Discharging Cycle " + str(B1_st/2))
                    B1_st-=1
                    pub1.publish(1) #switch to charging
        elif B1_st == 0:
            rospy.loginfo("Battery 1 Test Done!")
        if B2_st >0:
            if (B2_st % 2 == 0):
                if (val.Bat2_Curr <= 100): #charging is done
                    rospy.loginfo("Battery 2 Done Charging Cycle " + str(B2_st/2))
                    B2_st-=1
                    pub2.publish(2) #switch to discharge
            else:
                if(val.Bat2_Volt <= 10800): #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 2 Done Discharging Cycle " + str(B2_st/2))
                    B2_st-=1
                    pub2.publish(1) #switch to charging
        elif B2_st == 0:
            rospy.loginfo("Battery 2 Test Done!")
        if B3_st >0:
            if (B3_st % 2 == 0):
                if (val.Bat3_Curr <= 100): #charging is done
                    rospy.loginfo("Battery 3 Done Charging Cycle " + str(B3_st/2))
                    B3_st-=1
                    pub3.publish(2) #switch to discharge
            else:
                if(val.Bat3_Volt <= 10800): #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 3 Done Discharging Cycle " + str(B3_st/2))
                    B3_st-=1
                    pub3.publish(1) #switch to charging
        elif B3_st == 0:
            rospy.loginfo("Battery 3 Test Done!")
        if B4_st >0:
            if (B4_st % 2 == 0):
                if (val.Bat4_Curr <= 100): #charging is done
                    rospy.loginfo("Battery 4 Done Charging Cycle " + str(B4_st/2))
                    B4_st-=1
                    pub4.publish(2) #switch to discharge
            else:
                if(val.Bat4_Volt <= 10800): #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 4 Done Discharging Cycle " + str(B4_st/2))
                    B4_st-=1
                    pub4.publish(1) #switch to charging
        elif B4_st == 0:
            rospy.loginfo("Battery 4 Test Done!")

        rate.sleep()


if __name__ == '__main__':
    run()
