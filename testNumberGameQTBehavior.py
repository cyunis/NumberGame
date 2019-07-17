#!/usr/bin/env python
# encoding=utf8

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


def choose_behaviors(number, right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub):
    # while True:
    if 1:
        # print("Please type characters to show a certain behavior, input 0 to quit:")
        # number = sys.stdin.readline()
        # return
        if(number == 0):
        #quit
            abc=1
        elif(number == 1):
        #point
            gesturePlay_pub.publish("QT/point_front")
            emotionShow_pub.publish("QT/speechSay_pubing")
            time.sleep(5)
            #print('point is a problem')
        elif(number == 2):
        #hold
            gesturePlay_pub.publish("QT/show_QT")
            emotionShow_pub.publish("QT/speechSay_pubing")
            time.sleep(5)
            #print('hold')
        elif(number == 3):
        #challenge
            gesturePlay_pub.publish("QT/challenge")
            emotionShow_pub.publish("QT/speechSay_pubing")
            time.sleep(5)
            #print('challenge')
        elif(number == 4):
        #arm holding
            gesturePlay_pub.publish("QT/show_left")
            emotionShow_pub.publish("QT/speechSay_pubing")
            time.sleep(5)
            #print('arm holding')
        elif(number == 5):
        #arm back
            emotionShow_pub.publish("QT/calming_down")
            time.sleep(1)
            gesturePlay_pub.publish("QT/bored")
            time.sleep(4)
        elif(number == 6):
        #nod
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
            #print('nod')
        elif(number == 7):
        #confused
            right_arm = Float64MultiArray()
            right_arm.data = [40, -60, -90]
            right_pub.publish(right_arm)
            time.sleep(1)
            emotionShow_pub.publish("QT/confused")
            time.sleep(2)
            right_arm.data = [-90, -60, -30]
            right_pub.publish(right_arm)
            time.sleep(4)    
        elif(number == 8):
        #yawn
            gesturePlay_pub.publish("QT/yawn")
            time.sleep(0.8)
            emotionShow_pub.publish("QT/yawn") 
            time.sleep(4)
        elif(number == 9):
        #happy
            emotionShow_pub.publish("QT/happy")
            time.sleep(2)
        elif(number == 10):
        #surprise
            gesturePlay_pub.publish("QT/surprise")
            emotionShow_pub.publish("QT/surprise")
            time.sleep(4)
        elif(number == 11):
        #right
            gesturePlay_pub.publish("QT/happy")
            emotionShow_pub.publish("QT/happy")
            time.sleep(4)
        elif(number == 12):
        #angry
            gesturePlay_pub.publish("QT/angry")
            emotionShow_pub.publish("QT/angry")
            time.sleep(4)
        elif(number == 13):
        #fly kiss
            gesturePlay_pub.publish("QT/kiss")
            time.sleep(1)
            emotionShow_pub.publish("QT/kiss")
            time.sleep(4)
        elif(number == 14):
        #hug
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
        elif(number == 15):
        #hand clap
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
            time.sleep(4)   
        elif(number == 16):
        #touch head
            left_arm = Float64MultiArray()
            right_arm = Float64MultiArray()
            left_arm.data = [-80, -30,-90]
            right_arm.data = [80, -30,-90]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(3.3)
            emotionShow_pub.publish("QT/confused")
            left_arm.data = [-100, -40,-90]
            right_arm.data = [100, -40,-90]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(1)
            left_arm.data = [-80, -40,-90]
            right_arm.data = [80, -40,-90]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(1)
            left_arm.data = [-100, -40,-90]
            right_arm.data = [100, -40,-90]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(1)
            left_arm.data = [-80, -40,-90]
            right_arm.data = [80, -40,-90]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(1)
            left_arm.data = [90, -60,-30]
            right_arm.data = [-90, -60,-30]
            left_pub.publish(left_arm)
            right_pub.publish(right_arm)
            time.sleep(2)
        else:
            bca1=1

def feedback_function(wrist_angle, encourage_level, probability,tracking_var):
#parametric gestures
#track feedback over course of game

#initialize publishers
rospy.init_node('qt_robot_interface1') #unique node name
#motors
right_pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)
left_pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)
head_pub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)
#emotion
emotionShow_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)
#gesture
gesturePlay_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
#speech
speechSay_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
#audio
audioPlay_pub = rospy.Publisher('/qt_robot/audio/play', String, queue_size=10)

#wait for publisher/subscriber connections
wtime_begin = rospy.get_time()
while (audioPlay_pub.get_num_connections() == 0 or
    speechSay_pub.get_num_connections() == 0 or
    gesturePlay_pub.get_num_connections() == 0 or
    emotionShow_pub.get_num_connections() == 0 or
    right_pub.get_num_connections() == 0 or
    left_pub.get_num_connections() == 0 or
    head_pub.get_num_connections() == 0 ) :

    rospy.loginfo("waiting for subscriber connections")
    if rospy.get_time() - wtime_begin > 5.0:
        rospy.logerr("Timeout while waiting for subscribers connection!")
        sys.exit()
    rospy.sleep(1)

#setting up phrase dictionaries
#introduction dict
intro_dict = {1:'Nice to meet you, I\'m QT! What\'s your name? Want to play a game? Always do max effort with your motions!', 
                2:'Nice to meet you, I\'m QT! Let\'s play a game! Think of a number between 1 and 100. Always do max effort with your motions!',
                3:'Hi I\'m QT! I think we\'ll have fun together. Can you think of a number between 1 and 100? Always do max effort with your motions!', 
                4:'Remember I can talk but I don\'t understand what you are saying. Always do max effort with your motions!'}
#to encourage play during game 
encourage_dict = {1:'Good job!', 
                2:'Hooray! Let\'s play again!', 
                3:'Wow you\'re good at this!',
                4:'You\'re doing a great job!',
                5:'Wow this is hard you\'re good at this！'}
#to guess
guess_dict = {1: 'Is your number {}?',
                2: 'I guess {}. Did I guess your number?',
                3: 'Ok I think I know your number. Is it {}?'}
#higher or lower
second_dict = {1: 'Is your number higher than mine? Show me yes or no.',
                2:'Oh no I didnt get it. Did I guess lower than your number?',
                3: 'Hmm is your guess bigger than mine?'}
# #researcher can use this if participant not paying attention - needs button or researcher needs computer
# distraction_set = ['Hi please focus on me', 'Do you like to play games?',
#       'Let\'s keep playing.', 'I am sad when you ignore me.', 
#       'Why won\'t you play with me?','Don\'t touch me!',
#       'Want to hear a joke? Show me yes or no with your hand.'] 
# #for when partipicant makes an unclear gesture - needs button or researcher needs computer
# confusion_set = ['I don’t think I understand could you repeat that motion?', 'Let\'s try again so I can be sure.', 'No speechSay_pubing just show me with your motions.']
# #for when the game is too hard for the participant - needs button or researcher needs computer
# end_set = ['Hm maybe we should play a different game.', 'Would you like to take a break?',
#       'Let\'s take a break.', 'Don\'t be sad let\'s do something else!']



#introduction and explain rules
speechSay_pub.publish("Hello, my name is Q T Robot. What is your name?")
choose_behaviors(9,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
name = input('What is your name? ') #add talking gesture while QT says this
speechSay_pub.publish("Hi "+name+""" I would like to play a guessing game with you. 
    In the game I get to ask you questions, and you get to answer yes or no
    only by using a thumbs up or a thumbs down gesture with your right arm.
    Let's practice. Can you show me a thumbs up to say yes?""")
choose_behaviors(3,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
choose_behaviors(2,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
choose_behaviors(1,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
correctup = input('Was it a good thumbs up? ')
if correctup is 'yes':
    speechSay_pub.publish("Awesome! Now can you show me a thumbs down to say no?")
    choose_behaviors(3,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
correctdown = input('Was it a good thumbs down? ')
if correctdown is 'yes':
    speechSay_pub.publish("""Cool! During the game, please keep your hand in the 
        middle until I ask you a question. That means your thumb is pointing sideways, 
        not up or down! Remember to try as hard as you can to show me thumbs up 
        or thumbs down, so I can understand if you mean yes or no! If your thumb 
        is going the wrong way, just push the red button to move it back to the 
        middle. Remember to keep your hands in the middle when you are not answering 
        a question.  And just do your best. Can you show me yes if that’s ok?""")
    choose_behaviors(2,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(3,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(6,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(4,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(6,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(3,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    choose_behaviors(1,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)

#initialize variables
nocounter = 0
yescounter = 0
high = 101
low = -1

correctdown = 'yes'
#play game now
if correctdown is 'yes':
    speechSay_pub.publish("Lets play now! Please think of a number between 1 and 100.")
    choose_behaviors(6,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
start = input('What is your number? ') #type ok
speechSay_pub.publish("I'm thinking of your number.")
choose_behaviors(16,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)

while start < 101:
    half_range = int((high-low)/2)
    current = half_range+low
    random_add = random.randrange(-half_range,half_range) #never add on outside of the guessing range
    random_guess = random.randrange(1,len(guess_dict))
    QT = current+random_add
    random_talk = random.randrange(1,5)
    random_listen = random.randrange(5,9)
    random_encourage = random.randrange(9,12)
    random_other = random.randrange(13,17)
    #print("QT Guess is: "+str(QT))
    #print("Current is {} and random addition is {}.".format(current,random_add))
    #print("High is {} and low is {}.".format(high,low))
    speechSay_pub.publish(guess_dict[random_guess].format(QT))
    choose_behaviors(random_talk,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    val = input('Is my guess correct? (0 no, 1 yes) ')
# use # number = sys.stdin.readline()
# number.split()[0]
    if val is 0:
        speechSay_pub.publish(second_dict[random_guess])
        choose_behaviors(random_listen,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)    
        nocounter += 1
    #QT makes a sad face, or says something
        while True:
            val2 = input('higher(1) or lower(0)? ')
# use # number = sys.stdin.readline()
            if val2 is 1:
                low = QT
                yescounter += 1
                break
            if val2 is 0:
                high = QT
                nocounter += 1
                break
            else:
                aaaaaa = 1
         #    if val == 'c': #participant is confused, researcher types
            #   speechSay_pub.publish(confusion_set[random_phrase])
            #   emotionShow_pub.publish('ava_confused') #questioning face - needs special programming?
            #   rospy.sleep(3)
            # if val == 'd': #participant is distracted, researcher types
            #   speechSay_pub.publish(distraction_set[random_phrase])
            #   emotionShow_pub.publish('ava_diqust') #disappointed face
            #   rospy.sleep(3)
          #   if val == 'e': #game is too hard
                # speechSay_pub.publish(end_set[random_phrase])
                # emotionShow_pub.publish('ava_sad') #sad face
                # rospy.sleep(3)
            #speechSay_pub.publish(encourage_dict[random_guess])
            #choose_behaviors(random_encourage,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
    else:
        speechSay_pub.publish('I win!')
        choose_behaviors(random_encourage,right_pub, left_pub, head_pub, emotionShow_pub, gesturePlay_pub, speechSay_pub, audioPlay_pub)
        yescounter += 1
        print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter))
        print('I got it!')
        quit()
    # if val == 'c': #participant is confused, researcher types
    #   speechSay_pub.publish(confusion_set[random_phrase])
    #   emotionShow_pub.publish('QT/confused') #questioning face - needs special programming?
    #   rospy.sleep(3)
    # if val == 'd': #participant is distracted, researcher types
    #   speechSay_pub.publish(distraction_set[random_phrase])
    #   emotionShow_pub.publish('QT/bored') #disappointed face
    #   rospy.sleep(3)
    # if val == 'e': #game is too hard
    #   speechSay_pub.publish(end_set[random_phrase])
    #   emotionShow_pub.publish('QT/sad') #sad face
    #   rospy.sleep(3)
        

