#!/usr/bin/env python
# encoding=utf8

#------------------------------------------------------------------------------
# Example robot use with CoRDial
# Copyright (C) 2017 Elaine Schaertl Short
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------


#import modules
import random
import rospy
import os
import sys
import time
import string
from std_msgs.msg import String
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from thumb.msg import Res
import rosbag
from message_filters import ApproximateTimeSynchronizer, Subscriber
import csv
from heapq import nlargest
import roslib; roslib.load_manifest('cordial_example')
import rospy
from cordial_core import RobotManager


#initialize variables
frame = 0 #necessary? 2, 1, 0, -1
state = 0
button = 0
statelist = []
buttonlist = []
supinate = 0
pronate = 0
feedback_dict = {}
count = 1
#modify these for each subject from GAS interview
GAS_worst_sup = 10 #angle 0 - 90 
GAS_bad_sup = 20
GAS_normal_sup = 30 
GAS_good_sup = 40
GAS_best_sup = 50
GAS_worst_pro = -10 #angle -90 - 0
GAS_bad_pro = -20
GAS_normal_pro = -30
GAS_good_pro = -40
GAS_best_pro = -50
GAS_worst_suptime = 1 #time, sec?
GAS_bad_suptime = 2
GAS_normal_suptime = 3
GAS_good_suptime = 4
GAS_best_suptime = 5
GAS_worst_protime =  1 #time, sec?
GAS_bad_protime = 2
GAS_normal_protime = 3
GAS_good_protime = 4
GAS_best_protime = 5
hand = 'right' #change this if using left hand


#gesture functions
def choose_behaviors(number):
    global right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub
    #talking:1~6
    if(number == 1):
    #show_both_hands:9s
        emotionShow_pub.publish("QT/talking")
        gesturePlay_pub.publish("numbergame/talking1")
        rospy.sleep(9)
    elif(number == 2):
    #stretch_talk:8s
        gesturePlay_pub.publish("numbergame/talking2")
        emotionShow_pub.publish("QT/talking")
        rospy.sleep(8)
    elif(number == 3):
    #challenge:5s
        gesturePlay_pub.publish("QT/challenge")
        emotionShow_pub.publish("QT/talking")
        time.sleep(5)
    elif(number == 4):
    #show left and right:10s
        emotionShow_pub.publish("QT/talking")
        gesturePlay_pub.publish("numbergame/talking3")
        rospy.sleep(10)
    elif(number == 5):
    #teaching,10s
        emotionShow_pub.publish("QT/talking")
        gesturePlay_pub.publish("numbergame/talking4")
        rospy.sleep(10)   
    elif(number == 6):
    #teaching:10s
        emotionShow_pub.publish("QT/talking")
        gesturePlay_pub.publish("numbergame/talking5")
        rospy.sleep(10)
    elif(number == 7):
    #show:9s
        emotionShow_pub.publish("QT/talking")
        gesturePlay_pub.publish("numbergame/talking6")
        rospy.sleep(9)

    #listening:8~9
    elif(number == 8):
    #nod:4s
        head = Float64MultiArray()
        emotionShow_pub.publish("QT/showing_smile")
        head.data = [0,-10]
        head_pub.publish(head)
        time.sleep(1)
        head.data = [0,10]
        head_pub.publish(head)
        time.sleep(1)
        head.data = [0,0]
        head_pub.publish(head)
        time.sleep(2)
    elif(number == 9):
    #arm back smile:7s
        emotionShow_pub.publish("QT/calming_down")
        time.sleep(1)
        gesturePlay_pub.publish("QT/bored")
        time.sleep(6)    


    #guessing:10~12
    elif(number == 10):
    #confused:11s
        emotionShow_pub.publish("QT/confused")
        gesturePlay_pub.publish("numbergame/thinking1")
        rospy.sleep(11)
    elif(number == 11):
    #touch head:11s
        emotionShow_pub.publish("QT/confused")
        gesturePlay_pub.publish("numbergame/thinking2")
        rospy.sleep(11)
    elif(number == 12):
    #thinking:11s
        emotionShow_pub.publish("QT/confused")
        gesturePlay_pub.publish("numbergame/thinking3")
        rospy.sleep(11)


    #feedback and encouragement:13~16
    elif(number == 13):
    #surprise:5.5s
        gesturePlay_pub.publish("QT/surprise")
        emotionShow_pub.publish("QT/surprise")
        time.sleep(5.5)
    elif(number == 14):
    #happy:5s
        gesturePlay_pub.publish("QT/happy")
        emotionShow_pub.publish("QT/happy")
        time.sleep(5)
    elif(number == 15):
    #hug:6s
        left_arm = Float64MultiArray()
        right_arm = Float64MultiArray()
        emotionShow_pub.publish("QT/happy")
        left_arm.data = [-20, -10, -15]
        left_pub.publish(left_arm)
        right_arm.data = [20, -10, -15]
        right_pub.publish(right_arm)
        time.sleep(3)
        left_arm.data = [90, -60, -30]
        left_pub.publish(left_arm)
        right_arm.data = [-90, -60, -30]
        right_pub.publish(right_arm)
        time.sleep(3)
    elif(number == 16):
    #hand clap:8.8s
        left_arm = Float64MultiArray()
        right_arm = Float64MultiArray()
        emotionShow_pub.publish("QT/happy")
        left_arm.data = [10, -90, -30]
        left_pub.publish(left_arm)
        right_arm.data = [-10, -90, -30]
        right_pub.publish(right_arm)
        time.sleep(1.8)
        left_arm.data = [10, -90, -90]
        left_pub.publish(left_arm)
        right_arm.data = [-10, -90, -90]
        right_pub.publish(right_arm)
        time.sleep(1)
        left_arm.data = [10, -90, -30]
        left_pub.publish(left_arm)
        right_arm.data = [-10, -90, -30]
        right_pub.publish(right_arm)
        time.sleep(1)
        left_arm.data = [10, -90, -90]
        left_pub.publish(left_arm)
        right_arm.data = [-10, -90, -90]
        right_pub.publish(right_arm)
        time.sleep(1)
        left_arm.data = [10, -90, -30]
        left_pub.publish(left_arm)
        right_arm.data = [-10, -90, -30]
        right_pub.publish(right_arm)
        time.sleep(1)
        left_arm.data = [90, -60, -30]
        left_pub.publish(left_arm)
        right_arm.data = [-90, -60, -30]
        right_pub.publish(right_arm)
        time.sleep(3)


    #special_function:17~19
    elif(number == 17):
    #hi/bye:7s
        gesturePlay_pub.publish("QT/hi")
        emotionShow_pub.publish("QT/happy")
        time.sleep(7)
    elif(number == 18):
    #fly kiss:7.5s
        gesturePlay_pub.publish("QT/kiss")
        time.sleep(1)
        emotionShow_pub.publish("QT/kiss")
        time.sleep(6.5)
    elif(number == 19):
    #yawn:6.8s
        gesturePlay_pub.publish("QT/yawn")
        time.sleep(0.8)
        emotionShow_pub.publish("QT/yawn") 
        time.sleep(6)
    
    #rest
    elif(number == 20):
        abc =1

    else:
        print("Please use a correct number!")
        
        
def gesture_talk(num):
    i = 1
    previous = []
    while i <= num:
        a = random.randint(1, 7)
        if i>1 and a == previous[i-2]:
            previous.append(a+1)
            a+=1 #increment the value so it doesn't repeat
        else:
            previous.append(a)
        choose_behaviors(a)
        i = i + 1
    
def gesture_listen(num):
    i = 1
    previous = []
    while i <= num:
        a = random.randint(8, 9)
        if i>1 and a == previous[i-2]:
            previous.append(a+1)
            a+=1 #increment the value so it doesn't repeat
        else:
            previous.append(a)
        choose_behaviors(a)
        i = i + 1
    
def gesture_guess(num):
    i = 1
    previous = []
    while i <= num:
        a = random.randint(10, 12)
        if i>1 and a == previous[i-2]:
            previous.append(a+1)
            a+=1 #increment the value so it doesn't repeat
        else:
            previous.append(a)
        choose_behaviors(a)
        i = i + 1

def gesture_encourage(num):
    i = 1
    previous = []
    while i <= num:
        a = random.randint(13, 16)
        if i>1 and a == previous[i-2]:
            previous.append(a+1)
            a+=1 #increment the value so it doesn't repeat
        else:
            previous.append(a)
        choose_behaviors(a)
        i = i + 1


#encourage decision function
def encourage_score():
    score = 1
    return score


#script function
def dictionary_set():
    #setting up phrase dictionaries
    #to guess
    guess_dict = {1: 'Is {} right? Please show me a thumbs up or down.',
                    2: 'Ok I think I know your number. Is it {}?',
                    3: 'Is your number {}? Please show me yes or no.',
                    4: 'I guess {}. Did I guess your number?',
                    5: 'Am I wrong if I guess {}?',
                    6: 'Is {} the wrong guess?',
                    7: 'Is {} wrong? Please show me yes or no.',
                    8: 'I guess {} am I wrong?'}
#make sure name and number are in the right spot for every phrase - use 0 or 1 in the brackets to call in order
    #higher or lower
    second_dict = {1: 'Hey {} is your number higher than {}? Show me yes or no.',
                    2: 'Oh no, I guessed {1}. Did I guess bigger than your number {0}?',
                    3: 'Hmm is {} bigger than my number {}?',
                    4: 'Hey is your number higher than {1} {0}? Show me yes or no.',
                    5: 'Oh no {}, I guessed {}. Did I guess bigger than your number?',
                    6: 'Hmm {}, is {} bigger than my number?',
                    7: 'Hey is your number higher than {1}? Show me yes or no please {0}.',
                    8: 'Oh no, I guessed {1} {0}! Did I guess bigger than your number?',
                    9: 'Hmm tell me {} is {} bigger than my number?'} 
    #to encourage play during game 
    encourage_dict = {1: 'Good job {}!',
                    2: 'That was your best one so far! Keep up the good work {}!',
                    3: 'I can tell you are trying really hard {}, nice job!',
                    4: 'You are getting better at this {}, wow!',
                    5: 'I know this is hard {}, keep trying!',
                    6: 'Hooray! Let’s play again {}!',
                    7: 'Hey {}, good job!',
                    8: 'That was your best one so far {}! Keep up the good work!',
                    9: 'Hey {} I can tell you are trying really hard, nice job!',
                    10: 'Everyone, {} is getting better at this!',
                    11: 'Keep trying, I know this is hard {} but you got it!',
                    12: 'Hooray you did great {}!'} 
    clarify_dict = {1: 'Sorry {} I didn’t see that, could you repeat that answer for me please?',
                    2: 'I think that was a {yes/no} {}. If I’m right/wrong, could you make a thumbs {up/down} for me please?',
#when this line is called make sure to include the yes/no ^^ (just add more format(name, yes, up) <ex)
                    3: 'Could you please show me that answer again {}?',
                    4: 'Sorry I didn’t see that {}, could you repeat that answer for me please?',
                    5: 'I think that was a {yes/no}. If I’m {right/wrong} {} could you make a thumbs {up/down} for me please',
#when this line is called make sure to include the yes/no ^^ (just add more format(name, yes, up) <ex)
                    6: 'Hey {} could you please show me that answer again?'} 
    reward_dict = {1: 'Let’s party!',
                    2: 'I have a joke {}, why did a crocodile marry a chicken? Because crock-o-doodle-doodle is a good last name!',
                    3: 'What is your favorite color {}? Mine is blue.',
                    4: 'I like playing games with you {}, you’re very fun. Do you like playing with me?',
                    5: 'Let’s celebrate!',
                    6: 'I am happy to play games with you {}!'}
#should i make a reconnect dictionary?
    return guess_dict,second_dict,encourage_dict,clarify_dict,reward_dict


#feedback function
def feedback_function(thumb_angle, gesture_time, time, name):
    global speechSay_pub, encourage_dict, reward_dict, clarify_dict, feedback_dict, count, wrongcounter, supinate, pronate
    #give each item weights and combine weights to make a %
    #want reward to be 80-50% and encourage >80% always
    #camera angle, GAS (fatigue), history of gestures, # of prompts
    #camera angles should be matched to buckets on the GAS - need to see lit if standard #s for this (10% is 1, 20% is 2)
        #these should be the most important factors to weight
    #increase the encouragement when GAS, camera angle is worse and increase more if history shows a pattern of worsening    
    #if high number of rewards maybe dont need to increase encouragement as much
    #if a lot of clarification is needed, and bad history of gestures, more encouragement and more reward for lower GAS
    #if history of gestures is bad but shows one good case give a reward
    #history categories: 1)90% good and then 10% bad(sudden dip) 2)equal mixture of good or bad 3)no improvement 4)getting worse 5)getting better 6)90% bad then good
    #1, 3, 4 - more encouragement. 2 - varied encouragement (maybe getting bored?). 5, 6 - more reward + encouragement.
    #1, 6 - high weights.
    #prompt categories: 1)a lot of clarification 2)a little clarification 3)less encouragement than normal 4)a lot of reward 5)a little reward
    #1 - more encouragement (maybe tired?). 2 - more reward. 3 - varied encouragement.
    
    #make the buckets based on the GAS variables
    gestureis = 0
    #if thumb_angle <
    
    #split thumb_angle into pronation or supination
    if thumb_angle>0:
        supinate = thumb_angle #thumbs up
    if thumb_angle<0:
        pronate = thumb_angle #thumbs down
    #gesture_time should be set to reses.count(1) or .count(-1) for supination or pronation respectively
    
    #categorize the gesture into a bucket based on supinate, pronate, gesture_time, time, etc
    
    feedback_dict[count] = [supinate,pronate,gesture_time,time]
    print(feedback_dict)
    count += 1
#make sure the encouragement plays when it should - include graded cueing? (feedback @ failure) see stroke lit for affectiveness/optimal challenge
    #50 degrees is the threshold, determined by GAS
    if abs(thumb_angle) < 50:
        encourage_prob = 0.85 -abs(thumb_angle/100.0) + time/300.0 #smaller angle, worse performance/ longer time, more tired, more enc
        print("Encouragement prob: " + str(encourage_prob))
        if encourage_prob<0:
            print("Error: encourage_prob is 0!")
            encourage_prob = 0
        if encourage_prob>1:
            print("Error: encourage_prob is 1!")
            encourage_prob = 1
        enc_flag = random.randrange(1,100)
        if enc_flag<encourage_prob*100:
            random_encourage = random.randrange(1,len(encourage_dict))
            speechSay_pub.publish(encourage_dict[random_encourage].format(name))
            print(encourage_dict[random_encourage].format(name))            
#make sure the reward functions to be only at intermittant intervals - should be v selective
    else:
        for i in range(1, count-1):
            avg_angle += feedback_dict[i][0]
        avg_angle /= (count-2)
        reward_compare = feedback_dict[count-1][0]/avg_angle
        reward_current = 0.5 + abs(thumb_angle/100.0) + time/300.0 #larger angle, better performance/ longer the time playing, more reward
        if reward_compare>reward_current:
            reward_prob = reward_compare
        if reward_current>reward_compare and reward_compare>0.9: #0.9 is the ratio of how much decline between GAS scores (-10%)
            reward_prob = reward_current
        if reward_current>reward_compare:
            reward_prob = 0.5
        if reward_prob<0:
            print("Error: reward_prob is 0!")
            reward_prob = 0
        if reward_prob>1:
            print("Error: reward_prob is 1!")
            reward_prob = 1
        rew_flag = random.randrange(1,100)
        if rew_flag<reward_prob*100 and wrongcounter<10:
            random_rew = random.randrange(1,len(reward_dict))
            speechSay_pub.publish(reward_dict[random_rew].format(name))
            print(reward_dict[random_rew].format(name))
#        if wrongcounter>10:
#            random_clar = random.randrange(1,len(clarify_dict))
#            speechSay_pub.publish(clarify_dict[random_clar].format(name))


#camera+button (and feedback) functions
def isThumbUp_Down():
    #wait for 5s to get the best thumb input during 5s, get 50 results totally
    global start_time, name
    
    i = 1
    reses = []
    angles = []
    feed_flag = 1 # to prevent if the child wants to replay
    while(i<20):
#make sure this is tailored to each child (GAS?)
        # print i
        #get thumb messages
        msg = rospy.wait_for_message("/thumb_result",String)
        msg = str(msg.data)
        msg_list = msg.split('+')
        res_msg = int(msg_list[0])
        angle_msg = float(msg_list[1])
        reses.append(res_msg)
        angles.append(angle_msg)

#         ###comment out this section if beaglebone isn't running###
#         #get button messages
#         data = rospy.wait_for_message("/openwearable_new",String)
#         strdata = str(data)

#         # hacky split
#         val = strdata.split(':')
#         val = val[1].split('\\t')
#         temp = val[0].split('"')
        
#         global frame
#         global state
#         global button
#         global yescounter
#         global nocounter
#         global wrongcounter
        
#         frame = int(temp[1])
#         state = int(val[1])
#         button = int(val[2])
        
#         print(frame, state, button)
        
#         if button == 1:#you have trouble and want to replay
#             print("Ok! Please try again.")
#             i=0
#             reses = []
#             angles = []
#             feed_flag = 0
#         if button == -1:
#             #quit the game
#             #print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter)+". Number wrong: "+str(wrongcounter))
#             speechSay_pub.publish("OK! Thanks for playing with me! Bye-bye!")
#             choose_behaviors(17)
#             sys.exit()
#         ### -------------------- ###
            
        i = i+1
        if i ==5 and feed_flag == 1: #do feedback function
            feedback_function(abs(angle_msg),time.time()-start_time,name)
        time.sleep(0.1)
        
    print("finished")
    feedback_function(angle_msg,reses,time.time()-start_time,name) #don't abs(angle)
    if reses.count(1) > 10: #if thumbs up more than half the time
        angles = nlargest(10, angles)
        average_angle = sum(angles)/len(angles)
        return 1 #thumb is up
    elif reses.count(-1) > 10: #if thumbs down more than half the time
        angles = [ -x for x in angles]
        angles = nlargest(10, angles)
        average_angle = -sum(angles)/len(angles)
        return -1 #thumb is down
    else:
        return 0 #thumb is horizontal

def record_data(camera_angle,time,button,script,image_raw,QT_motor):
    assert camera_angle.header.stamp == time.header.stamp == button.header.stamp == script.header.stamp == image_raw.header.stamp == QT_motor.header.stamp
    print "got all QT data header.stamp matched"
    data_list = [camera_angle,time,button,script,image_raw,QT_motor]
    #use rosbag to record data
    #astra camera data/QT camera data/angle result data/button data/game playing data:sentence said by QT and children response
    #astra camera data should be recorded on the local computer, use compressed
    #QT camera just rosbag /image_raw
    #motion and sentences just rosbag moter topic and speech topic
    #button data just rosbag button data
    #print data_list
    with open('data_collection_file.csv', mode='w') as data_collection_file:
        data_writer = csv.writer(data_collection_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([camera_angle,time,button,script,image_raw,QT_motor])

ds = ApproximateTimeSynchronizer([camera_angle,time,button,script,image_raw,QT_motor], queue_size=5, slop=0.1) #slop is delay for synch in sec
    #the variables in the list ^^ should be the variable names from the subscriber nodes ex: Subscriber("/wide_stereo/left/image_rect_color", sensor_msgs.msg.Image
ds.registerCallback(record_data)


#orthosis/button/IMU subscriber function 
#see openWearable/ros/ow_subscriber.py for original script 
def callback():
    i=1
    while i<20:
        data = rospy.wait_for_message("/openwearable_new",String)
        strdata = str(data)

        # hacky split
        val = strdata.split(':')
        val = val[1].split('\\t')
        temp = val[0].split('"')
        global frame
        global state
        global button
        # global statelist
        # global buttonlist
        frame = int(temp[1])
        state = int(val[1])
        button = int(val[2])
        # statelist.append(state)
        # buttonlist.append(button)
        print(frame, state, button)
        i = i+1

        if button == 1:
            return 1
        if button == -1:
            return -1
    return 0
    
def listener():
    #global statelist
    #global buttonlist
    #statelist = []
    #buttonlist = []
    #rospy.init_node('listener', anonymous=True)
    #rospy.Subscriber('openwearable', String, callback)
    #rospy.sleep(3) #change sleep value to be amount of time to answer (5 sec?)
    pass


if __name__=="__main__":
    rospy.init_node("CoRDial_example")
    rm = RobotManager("DB1")
    rm.say("happy",wait=True) #use list in google docs
#add rm.say instead of speechSay_pub
    #name = 'guy'
    
    #initialize dictionary
    guess_dict,second_dict,encourage_dict,clarify_dict,reward_dict = dictionary_set()
    
    #initialize publishers
    rospy.init_node('qt_numbergame')
    right_pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)
    left_pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)
    head_pub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)
    #emotionShow_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)
    gesturePlay_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
    speechSay_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    audioPlay_pub = rospy.Publisher('/qt_robot/audio/play', String, queue_size=10)
    
    #wait for publisher connections
    wtime_begin = rospy.get_time()
    while (#audioPlay_pub.get_num_connections() == 0 or
        speechSay_pub.get_num_connections() == 0 or
        gesturePlay_pub.get_num_connections() == 0 or
        #emotionShow_pub.get_num_connections() == 0 or
        right_pub.get_num_connections() == 0 or
        left_pub.get_num_connections() == 0 or
        head_pub.get_num_connections() == 0 ) :
        rospy.loginfo("waiting for subscriber connections")
        if rospy.get_time() - wtime_begin > 5.0:
            rospy.logerr("Timeout while waiting for subscribers connection!")
            sys.exit()
        rospy.sleep(1)

    game_flag = 0 #set to 0 to play intro
    start_time = time.time()
    #name = 'Catherine'

    while 1: #game always running, until shutdown by children
        print("Do you want to play again please? Show me thumbs up/down.")
#edit ^ to not be the same every time
        res = isThumbUp_Down()

        if res == -1:
            #game over
            speechSay_pub.publish(("Thanks for playing with me {}! Bye-bye!").format(name))
            choose_behaviors(17)
            break
        elif res == 1:
            if game_flag == 0:#the first time to play
                #introduction
                speechSay_pub.publish("Hello, my name is Q T Robot. What is your name? ") #6.5 sec
                choose_behaviors(17)
                name = raw_input('What is your name? ')
                speechSay_pub.publish("Hi   "+name+""",      I would like to play a guessing game with you. 
                In the game  In the game, I ask you questions, and you answer yes or no by using a 
                thumbs up or a thumbs down with your     """ +hand+"""       hand. Let’s practice.  
                Can you show me a thumbs up to say yes?""") #22-25 sec
                gesture_talk(3)
                #configuration
                res = isThumbUp_Down()

                if res == 1:
                    speechSay_pub.publish("Awesome! Now can you show me a thumbs down to say no?") #6 sec
                    gesture_talk(1)
                res = isThumbUp_Down()

                if res == -1:
                    speechSay_pub.publish("""Thanks! During the game, please keep your hand flat on the 
                        arm rest until I ask you a question. If your thumb 
                        is going the wrong way, just push the green button. And just do your best. 
                        Can you please show me yes if that’s ok?""") #40.5 sec
                    gesture_talk(5)
            res = isThumbUp_Down()
            
            #initialize variables
            nocounter = 0
            yescounter = 0
            wrongcounter = 0
            high = 51
            low = -1
 
            if res == 1:
                #play game now
                speechSay_pub.publish("Let's play now! Please think of a number between 1 and 50.") #6.5 sec
                gesture_talk(1)
                start = input('What is your number? ') #type a number - no rospy.sleep because waiting for input
#we need to input this from camera computer and subscriber to get the number
                speechSay_pub.publish("I'm thinking of your number.") #3 sec
                gesture_guess(1)
                while start < 51:
                    half_range = int((high-low)/2)
                    current = half_range+low
                    random_add = random.randrange(-half_range,half_range) #never add on outside of the guessing range
                    QT = current+random_add
                    random_guess = random.randrange(1,len(guess_dict))
                    #ask if correct
                    speechSay_pub.publish(guess_dict[random_guess].format(QT)) 
                    print(guess_dict[random_guess].format(QT))    
                    choose_behaviors(2)
                    res = isThumbUp_Down()

                    if random_guess<5: #no means incorrect guess
                        incorrect = -1
                        print('no means incorrect')
                    else: #yes means incorrect guess
                        incorrect = 1
                        print('yes means incorrect')
                    if res == incorrect:
                        if QT == start: #prompt if they make a wrong answer about the correctness of QTs guess
                            random_clar = random.randrange(1,len(clar_dict))
                            speechSay_pub.publish(clarify_dict[random_clar].format(name))                         
                            gesture_talk(1)
                            wrongcounter += 1
                        else:
                            #ask if higher or lower
                            random_second = random.randrange(1,len(second_dict))
                            speechSay_pub.publish(second_dict[random_second].format(name,QT))
                            gesture_talk(1)                        
                            choose_behaviors(2)
                            nocounter += 1
                            while True:
                                res = isThumbUp_Down()

                                if res == 1:
                                    if QT > start:
                                        random_clar = random.randrange(1,len(clar_dict))
                                        speechSay_pub.publish(clarify_dict[random_clar].format(name))                         
                                        gesture_talk(1)
                                        wrongcounter += 1
                                    else:
                                        low = QT
                                        yescounter += 1
                                        break
                                if res == -1:
                                    if QT < start:
                                        random_clar = random.randrange(1,len(clar_dict))
                                        speechSay_pub.publish(clarify_dict[random_clar].format(name))
                                        print(clarify_dict[random_clar].format(name))                            
                                        gesture_talk(1)
                                        wrongcounter += 1
                                    else:
                                        high = QT
                                        nocounter += 1
                                        break #break from inner while loop
                                else:
                                    speechSay_pub.publish("Wrong input! Please input again.")
                    elif res == -incorrect:
                        speechSay_pub.publish('Hooray! I got it! Thanks' + name + 'for playing with me. Do you want to play again with me?') #9 sec
#vary this message. also should they play a minimum of 3 games mandatory, the rest optional? 
                        choose_behaviors(14)
                        yescounter += 1
                        print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter)+". Number wrong: "+str(wrongcounter))
                        game_flag = game_flag + 1
#put the record data call back here (and elsewhere?)
                        break
        else:
            speechSay_pub.publish("Wrong input! Please input again.")
#what should QT say?
