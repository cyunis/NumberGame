import transitions
import time
from transitions.extensions import GraphMachine as Machine
from feedback import statementRandomizer
from logger import Logger
import random
import pygraphviz
import sys
from std_msgs.msg import String
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from thumb.msg import Res
from heapq import nlargest
import copy

from message_filters import ApproximateTimeSynchronizer, Subscriber
import roslib; roslib.load_manifest('cordial_example')
import rospy
from cordial_core import RobotManager

class NumberGameInteraction:
    def __init__(self, use_qt_robot, leftHanded=False):
        self.start_recording = False


        rospy.init_node('qt_number_game')
        #set up publishers and subscribers
        #publishers
        self.audio_play_pub = rospy.Publisher('/qt_robot/audio/play', String, queue_size=10)

        self.right_pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)
        self.left_pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)
        self.head_pub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)

        self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        
        #subscribers
        self.thumb_sub = rospy.Subscriber("/thumb_result", String, self.process_thumb_data)
        self.beaglebone_sub = rospy.Subscriber("/openwearable_new", String, self.process_beaglebone_data)

        #data to measure
        self.start_time = time.time()
        self.number_of_completed_games = 0
        self.number_of_supinations = 0 #yes
        self.number_of_pronations = 0 #no
        self.isLeftHanded = False

        self.recording_start_time = self.start_time
        self.gesture_values = []

        self.average_thumb_value = 0
        self.gesture_time = 0
        self.GAS1 = 10 #degrees
        self.GAS2 = 20
        self.GAS3 = 30
        self.GAS4 = 40
        self.GAS5 = 50
        self.thumb_time = 5 #seconds

        #data to make game run smoothly
        self.statementRandomizer = statementRandomizer()
        self.robotManager = RobotManager('DB1')

        self.use_robot = use_qt_robot
        self.guess_lower_bound = 1
        self.guess_upper_bound = 50
        self.guesses = []
        self.number = 0
        self.ready_to_move_on = True
        self.is_aborted = False
        

    #callback functions
    def process_thumb_data(self, msg):
        
        if(self.start_recording == True):
            #save the previous recording
            self.gesture_values = []
            self.start_recording = False
            self.recording_start_time = time.time()

        data = str(msg.data)
        data_list = data.split('+')
        thumb_status = int(data_list[0]) # -1->thumbs down, 0->horizontal 1->thumbs up 
        thumb_angle = float(data_list[1]) # angle between 
        
        if(self.isLeftHanded == True):
            thumb_angle = -(thumb_angle - 180)

        self.gesture_values.append({'time': time.time() - self.recording_start_time, 'angle': thumb_angle})


    def process_beaglebone_data(self, msg):
        print('Received on beaglebone: ' + str(msg.data))

        if(str(msg.data) == 'abort'):
            self.robotManager.stop_speech()
            self.is_aborted = True
            self.abort()


    #helper functions to make sure that transitions are executed correctly
    def is_ready_to_move_on(self):
        #return whether or not the state machine can continue
        return self.ready_to_move_on


    def check_state_machine_status(self):
        if(self.is_aborted):
            raise ValueError('I should not be here')


    def reset_ready_to_move_on(self):
        self.play_gesture(8) #do small gestures at each transition ~= all the time
        #called after every transition is completed
        self.ready_to_move_on = False


    def guess_equals_number(self):
        return self.guesses[-1] == self.number

    def play_gesture(self, gesture_index):
        if(self.use_robot):
            gesture_name = self.statementRandomizer.chooseRandomStatement(gesture_index)
            print('playing gesture: {}'.format(gesture_name))
            if(gesture_name.startswith('gestures_programmed')):
                self.gestures_programmed(int(gesture_name.split('(')[1].split(')')[0]))
            else:
                self.gesture_pub.publish(gesture_name)


    def give_feedback(self):
        if(self.use_robot):
            self.play_gesture(12)
            self.robotManager.say(self.statementRandomizer.getResponseBehavior(self.average_thumb_value, self.gesture_time), wait=True)


    def get_guess_statement(self):
        print(self.statementRandomizer.chooseRandomStatement(0))


    def give_feedback_calculate_guess(self):
        self.give_feedback()
        self.calculate_guess()


    def get_thumb_data(self, duration):
        print('...................starting data collection..................')
        self.start_recording = True
        rospy.sleep(duration)
        values = copy.copy(self.gesture_values)
        
        self.play_gesture(11) #do gestures while waiting for answer
        
        print(values)

        num_above_thresh = 0
        supinate_angle_sum = 0 #yes
        num_below_thresh = 0
        pronate_angle_sum = 0 #no

        #check to see if the gesture passes the threshold for normal GAS score
        for value in values:
            if value['angle'] > self.GAS3:
                supinate_angle_sum += value['angle']
                num_above_thresh += 1
            elif value['angle'] < -self.GAS3:
                pronate_angle_sum += value['angle']
                num_below_thresh += 1

        if(num_below_thresh == 0 and num_above_thresh == 0):
            angle = 0
            time = 1
        elif( num_below_thresh < num_above_thresh):
            angle = supinate_angle_sum / num_above_thresh
            time = (num_above_thresh * duration) / len(values)
        else:
            angle = pronate_angle_sum / num_below_thresh
            time = (num_below_thresh * duration) / len(values)

        self.average_thumb_value = angle
        self.gesture_time = time

        print('angle: {}, time: {}'.format(self.average_thumb_value, self.gesture_time))



    #logic for each state transition
    def get_name(self):
        self.robotManager.say('intro1', wait=True)
        self.name = raw_input('what is their name?')
        if(self.name == 'abort'):
            self.abort()


    def give_instruction(self):
        #give instruction to the game
        
        print('you will play a simple thumbs up/down game with me!')


    def on_enter_practice_thumb_up(self):
        self.check_state_machine_status()
        #ask to demonstrate a thumbs up
        self.play_gesture(10)
        self.robotManager.say('intro2', wait=True)
        print('practice thumb up')
        self.get_thumb_data(self.thumb_time)
        print(self.average_thumb_value, self.gesture_time)
        self.ready_to_move_on = self.average_thumb_value > 0


    def practice_doesnt_go_up(self):
        #ask to try thumbs up again
        self.play_gesture(8) #small gestures for clarify
        self.robotManager.say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        print('try to put your thumb up again')


    def on_enter_practice_thumb_down(self):
        self.check_state_machine_status()
        #ask for a thumbs down
        self.play_gesture(10)
        self.robotManager.say('intro3', wait=True)
        print('practicing thumb down')
        self.get_thumb_data(self.thumb_time)
        self.ready_to_move_on = self.average_thumb_value < 0


    def practice_doesnt_go_down(self):
        #ask to try to put a thumbs down again
        self.play_gesture(8) #small gestures for clarify
        self.robotManager.say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True) #should have a condition to check for yes/no with different feedback sentences
        print('try to put your thumb down again')


    def on_enter_input_number(self):
        #secretly input the number
        self.play_gesture(10)
        self.robotManager.say('startgame', wait=True)
        self.check_state_machine_status()
        self.number = input('what is the number being guessed?')


    def calculate_guess(self):
        half_range = int((self.guess_upper_bound - self.guess_lower_bound)/2)
        ideal_guess = half_range+ self.guess_lower_bound
        guess = ideal_guess + random.randint(-half_range, half_range)
        while(guess in self.guesses):
            guess = ideal_guess + random.randint(-half_range, half_range)
        self.guesses.append(guess)


    def on_enter_make_guess(self):
        self.check_state_machine_status()

        #ask if the guessed number is correct
        self.play_gesture(9)
        statement_key = self.statementRandomizer.chooseRandomStatement(0)
        self.robotManager.say(statement_key+ '{}'.format(self.guesses[-1]), wait=True)
        modifier = 1 if statement_key[-1] in ['A', 'B', 'C', 'D'] else -1
        #get the angle measurements from the camera
        self.get_thumb_data(self.thumb_time)

        self.ready_to_move_on = modifier * self.average_thumb_value > 0


    def incorrect_guess_response(self):
        #try asking again
        self.play_gesture(8) #small gestures for clarify
        self.robotManager.say(self.statementRandomizer.chooseRandomStatement(1, self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        print('actually, let me ask in a different way...')


    def on_enter_higher_or_lower(self):
        self.check_state_machine_status()
        #ask if number is higher than the guess
        self.play_gesture(9)
        statement_key = self.statementRandomizer.chooseRandomStatement(6)
        self.robotManager.say( statement_key + '{}'.format(self.guesses[-1]), wait=True)

        print('guess is {}, actual is {}'.format(self.guesses[-1], self.number))
        #get angle measures from the camera
        self.get_thumb_data(self.thumb_time)

        if(self.guesses[-1] < self.number and self.average_thumb_value > 0):
            self.ready_to_move_on = True
            self.guess_lower_bound = self.guesses[-1]
        elif(self.guesses[-1] > self.number and self.average_thumb_value < 0):
            self.ready_to_move_on = True
            self.guess_upper_bound = self.guesses[-1]


    def incorrect_higher_lower(self):
        #try asking again
        self.play_gesture(10)
        self.robotManager.say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        print('hmmmm are you sure?')


    def give_feedback(self):
        if(self.use_robot):
            #say a random feedback statement
            self.play_gesture(12) #should be different gestures for different levels of feedback - or different faces on cordial?
            self.robotManager.say(self.statementRandomizer.getResponseBehavior(self.average_thumb_value, self.gesture_time), wait=True)


    def on_enter_play_again(self):
        self.check_state_machine_status()

        #say that QT won
        self.play_gesture(12)
        self.robotManager.say(self.statementRandomizer.chooseRandomStatement(7), wait=True)

        print(self.statementRandomizer.performedBehaviors)
        self.get_thumb_data(self.thumb_time)
        # res = input('woohoo I won, want to play again?')

        self.number_of_completed_games += 1
        self.guesses = []
        self.guess_lower_bound = 1
        self.guess_upper_bound = 50
        self.ready_to_move_on = self.average_thumb_value < 0


    def on_enter_end(self):
        #add the gesture for bye bye
        self.robotManager.say('statement14')
        print('thanks for playing!')
        print('stats: games played: {}\ntime played: {}'.format(self.number_of_completed_games, time.time()-self.start_time))
        sys.exit()


    def gestures_programmed(self, number):
        if(number == 1):
            #listening, nod:4s
            head = Float64MultiArray()
            head.data = [0,-10]
            head_pub.publish(head)
            time.sleep(1)
            head.data = [0,10]
            head_pub.publish(head)
            time.sleep(1)
            head.data = [0,0]
            head_pub.publish(head)
            time.sleep(2)
        elif(number == 2):
            #encouragement, hug:6s
            left_arm = Float64MultiArray()
            right_arm = Float64MultiArray()
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
        elif(number == 3):
            #encouragement, hand clap:8.8s
            left_arm = Float64MultiArray()
            right_arm = Float64MultiArray()       
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


states = ['get_name', 'practice_thumb_up', 'practice_thumb_down', 'input_number', 'make_guess', 'higher_or_lower', 'play_again', 'end']
transitions = [
                { 'trigger':'abort', 'source':'*', 'dest':'end'}, #all states go to the end if the button is pressed

                { 'trigger': 'advance', 'source': 'get_name', 'dest': 'practice_thumb_up', 'prepare':'get_name', 'before':'give_instruction'},

                { 'trigger': 'advance', 'source': 'practice_thumb_up', 'dest': 'practice_thumb_down', 'conditions':'is_ready_to_move_on' },
                { 'trigger': 'advance', 'source': 'practice_thumb_up', 'dest': 'practice_thumb_up', 'unless':'is_ready_to_move_on', 'before':'practice_doesnt_go_up'},

                { 'trigger': 'advance', 'source': 'practice_thumb_down', 'dest': 'input_number', 'conditions':'is_ready_to_move_on' },
                { 'trigger': 'advance', 'source': 'practice_thumb_down', 'dest': 'practice_thumb_down', 'unless':'is_ready_to_move_on', 'before':'practice_doesnt_go_down'},

                { 'trigger': 'advance', 'source': 'input_number', 'dest': 'make_guess', 'before':'calculate_guess' },

                { 'trigger': 'advance', 'source': 'make_guess', 'dest': 'play_again', 'conditions':['is_ready_to_move_on', 'guess_equals_number']},
                { 'trigger': 'advance', 'source': 'make_guess', 'dest': 'higher_or_lower', 'unless':['is_ready_to_move_on', 'guess_equals_number'], 'before':'give_feedback' },
                { 'trigger': 'advance', 'source': 'make_guess', 'dest': 'make_guess', 'conditions':'is_ready_to_move_on', 'unless':'guess_equals_number', 'before':'incorrect_guess_response' }, #participant says number is correct when it is not
                { 'trigger': 'advance', 'source': 'make_guess', 'dest': 'make_guess', 'conditions':'guess_equals_number', 'unless':'is_ready_to_move_on', 'before':'incorrect_guess_response' }, #participant says number is not correct when it is

                { 'trigger': 'advance', 'source': 'higher_or_lower', 'dest': 'make_guess', 'conditions':'is_ready_to_move_on',  'before':'give_feedback_calculate_guess' },
                { 'trigger': 'advance', 'source': 'higher_or_lower', 'dest': 'higher_or_lower', 'unless':'is_ready_to_move_on', 'before':'incorrect_higher_lower'},

                { 'trigger': 'advance', 'source': 'play_again', 'dest': 'end', 'conditions':'is_ready_to_move_on'},
                { 'trigger': 'advance', 'source': 'play_again', 'dest': 'input_number', 'unless':'is_ready_to_move_on'},
            ]

game = NumberGameInteraction(True)
machine = Machine(model=game, states=states, transitions=transitions, initial='get_name', before_state_change='reset_ready_to_move_on', show_state_attributes=True, show_conditions=True)
game.get_graph().draw('TommyThumbDiagram.png', prog='dot')

while(1):
    print(game.state)
    print('to')
    game.advance()
    print(game.state)
    print('---------')
