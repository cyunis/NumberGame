#!/usr/bin/env python
#code for the bisection number game, start with logical steps
#step 1: initialize variables, import modules, set up phrase lists
import random
import bisect
import sys
import rospy
from std_msgs.msg import String
rospy.init_node('qt_robot_interface1') #unique mode name
Talk1 = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size = 10)
while Talk1.get_num_connections() == 0:
    rospy.loginfo("Waiting for subscriber to connect")
    rospy.sleep(1) #teaching it to wait

#researcher will toggle some of these, some are scripted to toggle as game is played
#introduction set
intro_set = ['Nice to meet you, I\'m QT! What\'s your name? Want to play a game?', 
		'Nice to meet you, I\'m QT! Let\'s play a game! Think of a number between 1 and 100',
        'Hi I\'m QT! I think we\'ll have fun together. Can you think of a number between 1 and 100?', 
	    'Remember I can talk but I don\'t understand what you are saying.']
#to encourage play during game
encourage_set = ['Good job!', 'Hooray! Let\'s play again!', 'Wow you\'re good at this!',
		'You\'re doing a great job!','Wow this is hard you\'re good at this!']
#researcher can use this if participant not paying attention - needs button
distraction_set = ['Hi please focus on me', 'Do you like to play games?',
		'Let\'s keep playing.', 'I am sad when you ignore me.', 
		'Why won\'t you play with me?','Don\'t touch me!'] 
#for when partipicant makes an unclear gesture - needs button
confustion_set = ['I don’t think I understand could you repeat that motion?',
		'Let\'s try again so I can be sure.', 'No talking just show me with your motions.']
#for when the game is too hard for the participant - needs button
end_set = ['Hm maybe we should play a different game.', 'Would you like to take a break?',
		'Let\'s take a break.', 'Don\'t be sad let\'s do something else!']

#step 2: generate strings for first interactions,
#pull a random phrase from correct set
random_phrase_ix = random.randrange(0,len(intro_set))
Talk1.publish(intro_set[random_phrase_ix]) #QT says this
rospy.sleep(3) #allow QT to finish sentence
start = input('Let\'s start! ') #type ok

#step 3: ask if guess is correct, use bisection alg
Talk1.publish('Is this your guess?') 
rospy.sleep(1)
guess_list = [-1,101]
half_guess = int((guess_list[1]-guess_list[0])/2) #next 3 lines = fxn
guess = bisect.bisect(guess_list, half_guess)+half_guess
newbound = guess+guess_list[0]
Talk1.publish(str(newbound)) 

#step 4: read response from participant
#for now use button press

#step 5: repeat - make the game ongoing
#step 6: include QT - will need gestures and phrases
while start == 'ok':
	Talk1.publish('Is my guess correct?')
	rospy.sleep(1)
    val = input('Is my guess correct? ') 
    if val == 'no':
	#QT makes a sad face, or says something
		Talk1.publish('Is your number higher than my guess?')
        val2 = input('yes or no? ')
        if val2 == 'yes':
            guess_list = [guess,100]
        if val2 == 'no':
            guess_list = [0,guess]
     #    if val == 'c': #participant is confused, researcher types
    	# 	Talk1.publish(confusion_set[random_phrase_ix])
    	# 	rospy.sleep(3)
    	# if val == 'd': #participant is distracted, researcher types
    	# 	Talk1.publish(distraction_set[random_phrase_ix])
    	# 	rospy.sleep(3)
      #   if val == 'e': #game is too hard
    		# Talk1.publish(end_set[random_phrase_ix])
    		# rospy.sleep(3)
        half_guess = int((guess_list[1]-guess_list[0])/2)
        guess = bisect.bisect(guess_list, half_guess)+half_guess
        newbound = guess+guess_list[0]
        Talk1.publish('Is your guess' + str(newbound))
        rospy.sleep(2)
        Talk1.publish(encourage_set[random_phrase_ix])
        rospy.sleep(3)
    if val == 'yes':
        Talk1.publish('I win!')
	#QT dances happily
        quit()
    if val == 'c': #participant is confused, researcher types
    	Talk1.publish(confusion_set[random_phrase_ix])
    	rospy.sleep(3)
    if val == 'd': #participant is distracted, researcher types
    	Talk1.publish(distraction_set[random_phrase_ix])
    	rospy.sleep(3)
    if val == 'e': #game is too hard
    	Talk1.publish(end_set[random_phrase_ix])
    	rospy.sleep(3)
        
