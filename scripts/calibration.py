#!/usr/bin/env python
# encoding=utf8

import time
import rospy
import os
import math
import sys
import string
import logging
import csv
import io
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from thumb.msg import Res
from heapq import nlargest
#from logger import Logger
import numpy as np 
# curve-fit() function imported from scipy 
from scipy.optimize import curve_fit 
from matplotlib import pyplot as plt 

angles = []
status = []


def angle_measures():
    start = time.time()
    global angles
    global status

    #get thumb angle measures from the camera
    status = []
    angles = []
  
    print("Starting 5 second recording at "+str(time.time()))
    while(time.time() < start + 5): #run for 5 seconds
        msg = rospy.wait_for_message("/thumb_result",String)
        msg = str(msg.data)
        msg_list = msg.split('+')
        thumb_status = int(msg_list[0]) # -1->thumbs down, 0->horizontal 1->thumbs up 
        thumb_angle = float(msg_list[1]) # angle  
        status.append(thumb_status)
        angles.append(thumb_angle)
    
    print("Finishing 5 second recording at "+str(time.time()))
    
    return sum(angles)/len(angles)

    # #create x vector for curve fitting
    # x_a = np.linspace(0,len(angles), len(angles))
    # z = np.polyfit(x_a,angles,5)
    # f = np.poly1d(z)
    # #plot angle data
    # plt.plot(x_a,angles, 'o', color = 'red')
    # plt.plot(x_a,f(x_a),'--',color = 'blue')

    # plt.show()

def time_measures(avg_a,up):
    start = time.time()
    global angles
    global status

    #get thumb angle measures from the camera
    status = []
    angles = []
  
    print("Starting 5 second recording at "+str(time.time()))
    while(time.time() < start + 5): #run for 5 seconds
        msg = rospy.wait_for_message("/thumb_result",String)
        msg = str(msg.data)
        msg_list = msg.split('+')
        thumb_status = int(msg_list[0]) # -1->thumbs down, 0->horizontal 1->thumbs up 
        thumb_angle = float(msg_list[1]) # angle  
        status.append(thumb_status)
        angles.append(thumb_angle)
    
    print("Finishing 5 second recording at "+str(time.time()))
    
    tot = 0

    for i in angles:
        if(i>avg_a) and up: #thumbs up
            tot += 1
        if(i<avg_a) and not up: #thumbs down
            tot += 1
    
    tot = 5*(float(tot)/float(len(angles)))

    return(tot) 


if __name__=="__main__":
    rospy.init_node('calibration')
    upordown = 1 #1 for up, -1 for down
    global angles

    #find the average thumbs up value
    avg_a = angle_measures()
    raw_input("Press Enter to continue to tot up...") #python 2, wait
    up_angles = angles

    #find the time on task for thumbs up
    tot_up = time_measures(avg_a,1) #1 = up
    raw_input("Press Enter to continue to thumbs down...") #python 2, wait
    tot_up_angles = angles

    #find the average thumbs down value
    avg_down_a = angle_measures()
    raw_input("Press Enter to continue to tot down...") #python 2, wait
    down_angles = angles

    #find the time on task for thumbs down
    tot_down = time_measures(avg_down_a,0) #0 = down
    tot_down_angles = angles

    with open("/home/qtrobot/calibration.txt",'w+') as output:
        output.write("average up angle~"+str(avg_a)+"~average down angle~"+str(avg_down_a)+"\n")
        output.write("angle up set~"+str(up_angles)+"~angle down set~"+str(down_angles)+"\n")
        output.write("time on task supinate~"+str(tot_up)+"~time on task pronate~"+str(tot_down)+"\n")
        output.write("tot up angle set~"+str(tot_up_angles)+"~tot angle down set~"+str(tot_down_angles)+"\n")

