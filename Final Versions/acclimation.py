#!/usr/bin/env python
# encoding=utf8

import time
import rospy
import os
import math
import sys
import string
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


def sync_beaglebone():
    i = 1
    while(1):
        data = rospy.wait_for_message("/openwearable_new",String)

        strdata = str(data)
        # hacky split
        val = strdata.split(':')
        val = val[1].split('\\t')
        temp = val[0].split('"')
        
        time_bb = int(temp[1])
        sync = int(val[1])

        if sync == 1:
            print("Sync pin turned on!")
            return [1,time_bb]
        if sync == 0:
            i += 1
        if i == 30:
            print("Sync pin did nothing for 30 signals")
            return [0,time_bb] #if 30 signals were sent without syncing, break


def angle_measures():
    start = time.time()
    global angles
    global status

    #get thumb angle measures from the camera
    status = []
    angles = []
    velocities = []
    acceleration = []
    jerk = []
    timestep = 15 #15 hz pub rate
    rrad = .1*(math.pi)/180 #radius ~4 in~= .1 m, convert to rad
    
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

    #create x vector for curve fitting
    x_a = np.linspace(0,len(angles), len(angles))
    z = np.polyfit(x_a,angles,5)
    f = np.poly1d(z)
    # za = np.polyfit(x_a,angles,4)
    # zb = np.polyfit(x_a,angles,5)
    #plot angle data
    plt.plot(x_a,angles, 'o', color = 'red')
    plt.plot(x_a,f(x_a),'--',color = 'blue')
    # plt.plot(x_a,za,'--',color = 'red')
    # plt.plot(x_a,zb,'--',color = 'green')

    plt.show()

    

    #calculating velocity and jerk
    for a in range(len(angles)-1):
        v = (angles[a+1]-angles[a])*timestep*rrad #m/sec
        velocities.append(v)
    for v in range(len(velocities)-1):
        acc = (velocities[v+1]-velocities[v])*timestep*rrad
        acceleration.append(acc)
    for acc in range(len(acceleration)-1):
        j = (acceleration[acc+1]-acceleration[acc])*timestep*rrad
        jerk.append(j)

    # return sum(angles)/len(angles)
    return([max(angles), max(velocities), max(jerk)])


def time_measures():
    global angles
    global status
    ot = 0
    tot = 0
    x = 0
    y = 0

    print(status)

    try:
        ot_up = status.index(1)
    except ValueError:
        ot_up = 0
    
    try:
        ot_down = status.index(-1)
    except ValueError:
        ot_down = 0

    tot_up = status.count(1)*5/len(status)
    tot_down = status.count(-1)*5/len(status)

    return([ot_up,ot_down,tot_up,tot_down]) #tot should be sum of all angles above max score


if __name__=="__main__":
    rospy.init_node('acclimation')
    upordown = 1 #1 for up, -1 for down
    global angles

    # sync_time = sync_beaglebone() #if 1 the syncpin is on
    # syncpin = sync_time[0]
    # synctime = sync_time[1]
    # print(syncpin,synctime)

    [a,v,j] = angle_measures()
    [ot_up,ot_down,tot_up,tot_down] = time_measures()

    angle_scores = []
    velocity_scores = []
    jerk_scores = []
    onsettime_scores = []
    timeontask_scores = []
    per = .8

    if upordown == 1:
        ot = ot_up*5/len(angles)
        tot = tot_up
        print(ot_up,tot_up)
    else:
        ot = ot_down*5/len(angles)
        tot = tot_down

    for x in range(1,6):
        angle_scores.append(per*a)
        velocity_scores.append(per*v)
        jerk_scores.append(per*j)
        onsettime_scores.append(per*ot)
        timeontask_scores.append(per*tot)
        per+=.1
        
    print("Angle scores are: "+str(angle_scores))
    print("Velocity scores are: "+str(velocity_scores))
    print("Jerk scores are: "+str(jerk_scores))
    print("Onset time scores are: "+str(onsettime_scores))
    print("Time on task scores are: "+str(timeontask_scores))

