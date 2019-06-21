#!/usr/bin/env python
#code for the bisection number game, start with logical steps
#step 1: initialize variables, import modules
import random
import bisect
import sys
import rospy
from std_msgs.msg import String
rospy.init_node('qt_robot_interface1')
Talk1 = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size = 10)
while Talk1.get_num_connections() == 0:
    rospy.loginfo("Waiting for subscriber to connect")
    rospy.sleep(1) #teaching it to wait


#step 2: generate strings for first interactions,
#pull a random phrase from correct set
intro_set = ['Nice to meet you, I\'m QT! Let\'s play a game! Think of a number between 1 and 100',
             'Guess a number between 1 and 100!', 
	     'Remember I can talk but I don\'t understand what you are saying.']
random_phrase_ix = random.randrange(0,len(intro_set))
intro_string = intro_set[random_phrase_ix]
Talk1.publish(intro_string) #QT says this
	#have QT do relevant facial expression - can I use the examples without text?
start = input('Let\'s start! ') #type ok
print(intro_string) 
	#pause this until QT finishes talking

#step 3: ask if guess is correct, use bisection alg
print('Is this your guess?')
Talk1.publish('Is this your guess?') 
	#QT says this
	#QT does relevant face/gesture
guess_list = [-1,101]
half_guess = int((guess_list[1]-guess_list[0])/2) #next 3 lines = fxn
guess = bisect.bisect(guess_list, half_guess)+half_guess
isit = str(guess+guess_list[0]) 
Talk1.publish(isit) 
	#QT says this

#step 4: read response from participant
#for now use button press

#step 5: repeat - make the game ongoing
while start == 'ok':
    val = input('Is my guess correct? ') 
	#pause this until QT finishes talking
    if val == 'no':
	#QT makes a sad face, or says something
        val2 = input('higher or lower? ')
	#QT says this
        if val2 == 'higher':
            guess_list = [guess,100]
        if val2 == 'lower':
            guess_list = [0,guess]
        half_guess = int((guess_list[1]-guess_list[0])/2)
        guess = bisect.bisect(guess_list, half_guess)+half_guess
        print(guess+guess_list[0])
	#QT says "i guess this now!" ^ or some other phrase w/ face
    if val == 'yes':
        print('I win!')
	#QT says this and dances happily
        quit()
        
#step 6: include QT - will need gestures and phrases
#this means that we will have input strings for QT and output strings (as voice)
#and code (for behavior)
#have adam show me how to make the conversation lines and pull motion library



