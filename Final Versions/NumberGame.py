#!/usr/bin/env python
# encoding: utf-8

#import modules
import random
import rospy
import os
import sys
import time
import string
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from thumb.msg import Res
import rosbag
from heapq import nlargest

#initialize variables
frame = 0 #necessary? 2, 1, 0, -1
state = 0
button = 0
statelist = []
buttonlist = []


#encourage decision function
def encourage_score():
    score = 1
    return score


#script function
def dictionary_set():
    #setting up phrase dictionaries
    #to guess
    guess_dict = {1: 'Is your number {}?', #2.5 sec
                    2: 'I guess {}. Did I guess your number?', #5.5 sec
                    3: 'Ok I think I know your number. Is it {}?', #5.5 sec
                    4: 'Is {} right?'} #2.5 sec
    #higher or lower
    second_dict = {1: 'Hey {} is your number higher than mine? Show me yes or no.', #7 sec 
                    2: 'Oh no I didn’t get it. Did I guess higher than your number {}?', #7 sec
                    3: 'Hmm is your guess bigger than mine {}?'} #4 sec  
    #to encourage play during game 
    encourage_dict = {1:'Good job {}!', #2.5 sec
                    2:'That was your best one so far! Keep up the good work {}!', #7 sec
                    3:'I can tell you are trying really hard {}, nice job!', #5 sec
                    4:'You are getting better at this {}, wow!', #4 sec
                    5:'I know this is hard {}, keep trying!'} #4.5 sec
    clarify_dict = {1: 'I didn’t see that {}, could you repeat that answer for me?', #6 sec
                    2: 'I think that was a {}. If I’m right could you make a thumbs up/down for me?', #6.5 sec
                    3: 'Could you show me that answer again {}?'} #4 sec 
    reward_dict = {1: 'Let’s dance.', #2 sec
                    2: 'I have a joke {}, why did a crocodile marry a chicken? Because crock-o-doodle-doodle is a good last name!', #9.5 sec
                    3: 'What is your favorite color {}? Mine is blue.', #5.5 sec
                    4: 'I like playing games with you {}, you’re very fun. Do you like playing with me?'} #8 sec
    return guess_dict,second_dict,encourage_dict,clarify_dict,reward_dict


#feedback function
def feedback_function(thumb_angle, time, name):
    global speechSay_pub, encourage_dict, reward_dict
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

    #50 degrees is the threshold, determined by GAS
    if abs(thumb_angle) < 50:
        encourage_prob = 0.85 -abs(thumb_angle/100.0) + time/300.0 #smaller angle, worse performance/ longer time, more tired, more enc
        if encourage_prob<0:
            print("Error: encourage_prob is 0!")
            encourage_prob = 0
        if encourage_prob>1:
            print("Error: encourage_prob is 1!")
            encourage_prob = 1
        enc_flag = random.randrange(1,100)
        if enc_flag<encourage_prob*100:
            random_encourage = random.randrange(1,len(encourage_dict))
            print(encourage_dict[random_encourage].format(name))
            rospy.sleep(7)

    else:
        reward_prob = 0.5 + abs(thumb_angle/100.0) + time/300.0 #larger angle, better performance/ longer the time playing, more reward
        if reward_prob<0:
            print("Error: reward_prob is 0!")
            reward_prob = 0
        if reward_prob>1:
            print("Error: reward_prob is 1!")
            reward_prob = 1
        rew_flag = random.randrange(1,100)
        if rew_flag<reward_prob*100:
            random_rew = random.randrange(1,len(reward_dict))
            print(reward_dict[random_rew].format(name))
            rospy.sleep(9)


#camera functions
def get_thumb_input():
    # print("enter")
    #wait for 5s to get the best thumb input during 5s, get 50 results totally
    i = 1
    reses = []
    angles = []
    while(i<40):
        # print i
        msg = rospy.wait_for_message("/thumb_result",String)
        msg = str(msg.data)
        msg_list = msg.split('+')
        res_msg = int(msg_list[0])
        angle_msg = float(msg_list[1])
        reses.append(res_msg)
        angles.append(angle_msg)
        i = i+1
        time.sleep(0.1)
    print("down")
    return reses,angles

def isThumbUp_Down():
    #add callback function
    #return up or down and the angle
    reses, angles = get_thumb_input()
    if reses.count(1) > 15:
        angles = nlargest(10, angles)
        res = sum(angles)/len(angles)
        return 1, res
    elif reses.count(-1) > 15:
        angles = [ -x for x in angles]
        angles = nlargest(10, angles)
        res = -sum(angles)/len(angles)
        return -1,res
    else:
        return 0,sum(angles)/len(angles)


#data collection function
def record_data():
    #use rosbag to record data:
    #astra camera data/QT camera data/angle result data/button data/game playing data:sentence said by QT and children response
    #astra camera data should be recorded on the local computer, use compressed
    #QT camera just rosbag /image_raw
    #QT behavior: moter, speech, and emotion topic
        #parametric position of joints
    #QT speech string
    #number of yes, no, button presses (wrong answer)
    #feedback function measurements - thumb angle, name, time, history of gestures, number of clarification/reward/encouragement
    #number of games played
    #any experimenter interventions or errors

    #air pressure, button, orthosis, fram data (done on beaglebone separately)
    pass


#orthosis/button/IMU subscriber function
#see openWearable/ros/ow_subscriber.py for original script 
def callback():
    i=1
    while i<20:
        data = rospy.wait_for_message("/openwearable",String)
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
    
        time.sleep(0.1)
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
    #initialize dictionary
    guess_dict,second_dict,encourage_dict,clarify_dict,reward_dict = dictionary_set()
    
    game_flag = 0 #set to 0 to play intro
    start_time = time.time()
    #name = 'Catherine'

    while 1:
        #game always running, until shutdown by children
        # exit_msg = rospy.wait_for_message()
        # if exit_msg.flag == False:
        # once_again = raw_input('Play again? ') #type 'yes' or 'no'
            # use # number = sys.stdin.readline() if prompt
                # number.split()[0]
        print("Do you want to play again? Show me thumbs up/down.")
#edit ^ to not be the same every time
        res, the_angle = isThumbUp_Down()
        # if once_again == 'no':
        if res == -1:
            #game over
            print("I had a great time with you today. Bye-bye!")
            break
        # elif once_again == 'yes':
        elif res == 1:
            if game_flag == 0:#the first time to play
                #introduction
                print("Hello, my name is T Q Computer. What is your name? ") 
                name = raw_input('What is your name? ')
                print("Hi   "+name+""",      I would like to play a guessing game with you. 
                In the game I get to ask you questions, and you get to answer yes or no
                only by using a thumbs up or a thumbs down gesture with your right arm.
                Let's practice. Can you show me a thumbs up to say yes?""")
                #configuration
                # correctup = raw_input('Please do a thumb up! ')
                print("Please do a thumbs up!")
                res, the_angle = isThumbUp_Down()
                # if correctup == 'up':
                if res == 1:
                    print("Awesome! Now can you show me a thumbs down to say no?")
                # correctdown = raw_input('Please do a thumb down! ')
                print("Please do a thumbs down!")
                res, the_angle = isThumbUp_Down()
                # if correctdown == 'down':
                if res == -1:
                    print("""Cool!! During the game, please keep your hand in the 
                        middle until I ask you a question. That means your thumb is pointing sideways, 
                        not up or down! Remember to try as hard as you can to show me thumbs up 
                        or thumbs down, so I can understand if you mean yes or no! If your thumb 
                        is going the wrong way, just push the red button to move it back to the 
                        middle. Remember to keep your hands in the middle when you are not answering 
                        a question.  And just do your best. Can you show me yes if that’s ok?""")
            
            #initialize variables
            nocounter = 0
            yescounter = 0
            wrongcounter = 0
            high = 51
            low = -1

            # correctok = raw_input('Please do a thumbs up to say OK! ')
            print("Please do a thumbs up to say OK!")
            res, the_angle = isThumbUp_Down()
            # if correctok == 'OK':
            if res == 1:
                #play game now
                print("Let's play now! Please think of a number between 1 and 50.") #6.5 sec
                start = input('What is your number? ') #type a number - no rospy.sleep because waiting for input
#we need to input this from camera computer and subscriber to get the number
                print("I'm thinking of your number.") #3 sec
                while start < 51:
                    half_range = int((high-low)/2)
                    current = half_range+low
                    random_add = random.randrange(-half_range,half_range) #never add on outside of the guessing range
                    QT = current+random_add
                    random_guess = random.randrange(1,len(guess_dict))
                    #ask if correct
                    print(guess_dict[random_guess].format(QT))    
                    print("Answer me with a thumbs up or down"+str(name))
#incorporate the instruction randomly (or just the first few times?) to remind them of the instructions
                    #val = input(guess_dict[random_guess].format(QT))
                    res, the_angle = isThumbUp_Down()

#remove the following lines for the button state and put in isThumbUp_Down()
                    button_state = callback()
                    if button_state == 1:
                        print("I am having trouble.")
                        print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter)+". Number wrong: "+str(wrongcounter))
                        speechSay_pub.publish("OK! I had a great time with you today. Bye-bye!")
                        choose_behaviors(16)
                        sys.exit()
#which loop does sys exit from?
                    feedback_function(the_angle,time.time()-start_time,name)
                    # if val == 'no':
                    if res == -1:
                        if QT == start: #prompt if they make a wrong answer about the correctness of QTs guess
                            print(clarify_dict[random_guess].format(name))
                            wrongcounter += 1
                        else:
                            #ask if higher or lower
                            print(second_dict[random_guess].format(name))
                            print("My guess is "+str(QT))
#should kids be reminded of the guess every time? if so needs to be randomized                           
                            nocounter += 1
                            while True:
                                # val2 = input('yes(1) or no(0)? ')
                                print("Please do a thumbs up/down to say higher or lower")
#how many times should kids be reminded of this?
                                feedback_function(the_angle,time.time()-start_time,name)
                                res, the_angle = isThumbUp_Down()
                                # if val2 == 1:
                                if res == 1:
                                    if QT > start:
                                        print(clarify_dict[random_guess].format(name))
                                        wrongcounter += 1
                                        feedback_function(the_angle,time.time()-start_time,name)
                                    else:
                                        low = QT
                                        yescounter += 1
                                        break
                                # if val2 == 0:
                                if res == -1:
                                    if QT < start:
                                        print(clarify_dict[random_guess].format(name))
                                        wrongcounter += 1
                                        feedback_function(the_angle,time.time()-start_time,name)
                                    else:
                                        high = QT
                                        nocounter += 1
                                        break #break from inner while loop
                                else:
                                    print("Wrong input! Please input again.")
#what should QT say?
                           
                    # elif val == 'yes':
                    elif res == 1:
                        print('Hooray! I got it! Thanks for playing with me. Do you want to play again with me?') #9 sec
#vary this message. also should they play a minimum of 3 games mandatory, the rest optional?
                        yescounter += 1
                        print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter)+". Number wrong: "+str(wrongcounter))
                        print('I got it!')
                        game_flag = game_flag + 1
                        break


                    # else:#child can input something except 'yes' and 'no' to break out the game
                    #     #game over
                    #     listener()
                    #     if 1 in buttonlist:
                    #         print("I am having trouble.")
                    #     print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter)+". Number wrong: "+str(wrongcounter))
                    #     speechSay_pub.publish("OK! I had a great time with you today. Bye-bye!")
                    #     choose_behaviors(16)
                    #     sys.exit()
        else:
            print("Wrong input! Please input again.")
#what should QT say?