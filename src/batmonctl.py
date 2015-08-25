#!/usr/bin/env python

# This code will control the battery test station

import rospy
import time
from std_msgs.msg import UInt8
from batmon.msg import bat_data
import subprocess
import os
import signal


#How many full charge- discharge cycles to do, even numbers ONLY!!!
Cycles = 2

avg = None

rosserial = subprocess.Popen(["roslaunch rosserial_server serial.launch"], shell=True, preexec_fn=os.setsid)
time.sleep(2)
Battery = raw_input('\n\nScan or Enter KF Battery Serial: ')
rosbag = subprocess.Popen(["rosbag record -a -j -O" + Battery], shell=True, preexec_fn=os.setsid)

def callback(data):
    global avg
    avg = data
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

    while avg == None:
        rospy.loginfo("Waiting for first reading")
        time.sleep(0.5)

    time.sleep(5)

    #Check if battery present, Start charging
    if (avg.Bat1_Volt > 5000):
        pub1.publish(1)
    else:
        B1_st = -1
        rospy.loginfo("Battery 1 not connected")
    if (avg.Bat2_Volt > 5000):
        pub2.publish(1)
    else:
        B2_st = -1
        rospy.loginfo("Battery 2 not connected")
#    if (val.Bat3_Volt > 5000):
#        pub3.publish(1)
#    else:
#        B3_st = -1
#        rospy.loginfo("Battery 3 not connected")
#    if (val.Bat4_Volt > 5000):
#        pub4.publish(1)
#    else:
#        B4_st = -1
#        rospy.loginfo("Battery 4 not connected")
    
    time.sleep(5) # Time for first charge to take hold
    
    val = bat_data

    while not rospy.is_shutdown():
       

        if B1_st >0:
            if (B1_st % 2 == 0):
                if ((val.Bat1_Curr <= 100) & (avg.Bat1_Curr <= 100)): #charging is done
                    rospy.loginfo("Battery 1 Done Charging Cycle " + str(Cycles - B1_st/2))
                    B1_st-=1
                    pub1.publish(2) #switch to discharge
            else:
                if((val.Bat1_Volt <= 10800) & (avg.Bat1_Volt <= 10800)): 
                #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 1 Done Discharging Cycle " + str(Cycles - B1_st/2 -1))
                    B1_st-=1
                    pub1.publish(1) #switch to charging
        elif B1_st == 0:
            rospy.loginfo("Battery 1 Test Done!")
        if B2_st >0:
            if (B2_st % 2 == 0):
                if ((val.Bat2_Curr <= 100)& (avg.Bat2_Curr <= 100)): #charging is done
                    rospy.loginfo("Battery 2 Done Charging Cycle " + str(Cycles - B2_st/2))
                    B2_st-=1
                    pub2.publish(2) #switch to discharge
            else:
                if((val.Bat2_Volt <= 10800) & (avg.Bat2_Volt <= 10800)): 
                #discharging is done when voltage less than 10.8V
                    rospy.loginfo("Battery 2 Done Discharging Cycle " + str(Cycles - B2_st/2 -1))
                    B2_st-=1
                    pub2.publish(1) #switch to charging
        elif B2_st == 0:
            rospy.loginfo("Battery 2 Test Done!")
#        if B3_st >0:
#            if (B3_st % 2 == 0):
#                if (val.Bat3_Curr <= 100): #charging is done
#                    rospy.loginfo("Battery 3 Done Charging Cycle " + str(B3_st/2))
#                    B3_st-=1
#                    pub3.publish(2) #switch to discharge
#            else:
#                if(val.Bat3_Volt <= 10800): #discharging is done when voltage less than 10.8V
#                    rospy.loginfo("Battery 3 Done Discharging Cycle " + str(B3_st/2))
#                    B3_st-=1
#                    pub3.publish(1) #switch to charging
#        elif B3_st == 0:
#            rospy.loginfo("Battery 3 Test Done!")
#        if B4_st >0:
#            if (B4_st % 2 == 0):
#                if (val.Bat4_Curr <= 100): #charging is done
#                    rospy.loginfo("Battery 4 Done Charging Cycle " + str(B4_st/2))
#                   B4_st-=1
#                    pub4.publish(2) #switch to discharge
#            else:
#                if(val.Bat4_Volt <= 10800): #discharging is done when voltage less than 10.8V
#                    rospy.loginfo("Battery 4 Done Discharging Cycle " + str(B4_st/2))
#                    B4_st-=1
#                    pub4.publish(1) #switch to charging
#        elif B4_st == 0:
#            rospy.loginfo("Battery 4 Test Done!")

        #Average the noisy val data
        val = avg

        # Kill other processes
        if ((B1_st ==0) & (B2_st == 0)):
            pub1.publish(1) #switch to charging
            pub2.publish(1) #switch to charging
            os.killpg(rosserial.pid, signal.SIGINT)
            os.killpg(rosbag.pid, signal.SIGINT)
            break

        rate.sleep()


if __name__ == '__main__':
    run()
