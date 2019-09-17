import transitions
import time
from transitions.extensions import GraphMachine as Machine
from feedback import statementRandomizer
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
        
        #subscribers
        self.thumb_sub = rospy.Subscriber("/thumb_result", String, self.process_thumb_data)
        self.beaglebone_sub = rospy.Subscriber("/openwearable_new", String, self.process_beaglebone_data)



        #data to measure
        self.start_time = time.time()
        self.number_of_completed_games = 0
        self.number_of_supinations = 0
        self.number_of_pronations = 0
        self.isLeftHanded = False

        self.recording_start_time = self.start_time
        self.gesture_values = []

        self.average_thumb_value = 0
        self.gesture_time = 0

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
            self.is_aborted = True
            self.abort()
        
        


        

    #helper functions to make sure that transitions are executed correctly
    def is_ready_to_move_on(self):
        #return whether or not the state machine can continue
        return self.ready_to_move_on

    def has_been_aborted(self):
        return self.is_aborted

    def reset_ready_to_move_on(self):
        #called after every transition is completed
        self.ready_to_move_on = False

    def guess_equals_number(self):
        return self.guesses[-1] == self.number

    def give_feedback(self):
        if(self.use_robot):
            print(self.statementRandomizer.getResponseBehavior(self.thumb_angle, self.gesture_time))

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
        
        print(values)

        num_above_thresh = 0
        pronate_angle_sum = 0
        num_below_thresh = 0
        supinate_angle_sum = 0

        for value in values:
            if value['angle'] > 30:
                pronate_angle_sum += value['angle']
                num_above_thresh += 1
            elif value['angle'] < -30:
                supinate_angle_sum += value['angle']
                num_below_thresh += 1
        
        angle = 0
        time = 5
        if(num_below_thresh == 0 or num_above_thresh == 0):
            angle = 0
            time = 1
        elif( num_below_thresh < num_above_thresh):
            angle = pronate_angle_sum / num_above_thresh
            time = (num_above_thresh * duration) / len(values)
        else:
            angle = supinate_angle_sum / num_below_thresh
            time = (num_below_thresh * duration) / len(values)

        #return angle and time
        return angle, time



        
        



    #logic for each state transition
    def get_name(self):
        self.name = raw_input('what is their name?')
        if(self.name == 'abort'):
            self.abort()

    def give_instruction(self):
        self.robotManager.say('statement3', wait=True)
        print('you will play a simple thumbs up/down game with me!')

    def on_enter_practice_thumb_up(self):
        self.robotManager.say('statement4', wait=True)
        print('practice thumb up')
        angle, time = self.get_thumb_data(5)
        print(angle, time)
        self.ready_to_move_on = angle > 0

    def practice_doesnt_go_up(self):
        self.robotManager.say('statement10', wait=True)
        print('try to put your thumb up again')

    def on_enter_practice_thumb_down(self):
        self.robotManager.say('statement1', wait=True)
        print('practicing thumb down')
        angle, time = self.get_thumb_data(5)
        self.ready_to_move_on = angle < 0

    def practice_doesnt_go_down(self):
        print('try to put your thumb down again')

    def on_enter_input_number(self):
        self.number = input('what is the number being guessed?')

    def calculate_guess(self):
        half_range = int((self.guess_upper_bound - self.guess_lower_bound)/2)
        ideal_guess = half_range+ self.guess_lower_bound
        guess = ideal_guess + random.randint(-half_range, half_range)
        while(guess in self.guesses):
            guess = ideal_guess + random.randint(-half_range, half_range)
        self.guesses.append(guess)

    def on_enter_make_guess(self):
        # res = input('{}: is {} your number?'.format(self.statementRandomizer.chooseRandomStatement(0),self.guesses[-1]))
        angle, time = self.get_thumb_data(5)
        self.ready_to_move_on = angle > 0

    def incorrect_guess_response(self):
        print('actually, let me ask in a different way...')

    def on_enter_higher_or_lower(self):
        print('is your number higher or lower than {}? (number is {})'.format(self.guesses[-1], self.number))
        # res = input('higher?')
        angle, time = self.get_thumb_data(5)

        if(self.guesses[-1] < self.number and angle > 0):
            self.ready_to_move_on = True
            self.guess_lower_bound = self.guesses[-1]
        elif(self.guesses[-1] > self.number and angle < 0):
            self.ready_to_move_on = True
            self.guess_upper_bound = self.guesses[-1]

    def incorrect_higher_lower(self):
        print('hmmmm are you sure?')

    def give_feedback(self):
        if(self.use_robot):
            print(self.statementRandomizer.getResponseBehavior(random.randint(1,60), random.randint(1,60)*0.1))


    def on_enter_play_again(self):
        print(self.statementRandomizer.performedBehaviors)
        angle, time = self.get_thumb_data(5)
        # res = input('woohoo I won, want to play again?')

        self.number_of_completed_games += 1
        self.guesses = []
        self.guess_lower_bound = 1
        self.guess_upper_bound = 50
        self.ready_to_move_on = angle < 0

    def on_enter_end(self):
        self.robotManager.stop_speech()
        self.robotManager.say('statement14')
        print('thanks for playing!')
        print('stats: games played: {}\ntime played: {}'.format(self.number_of_completed_games, time.time()-self.start_time))
        sys.exit()



states = ['get_name', 'practice_thumb_up', 'practice_thumb_down', 'input_number', 'make_guess', 'higher_or_lower', 'play_again', 'end']
transitions = [
                { 'trigger':'abort', 'source':'*', 'dest':'end'}, #all states go to the end if the button is pressed
                { 'trigger':'advance', 'source':'[get_name, practice_thumb_up, practice_thumb_down, input_number, make_guess, higher_or_lower, play_again]', 'dest':'end', 'conditions':'has_been_aborted'}, #all states go to the end we have pressed the button

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
                { 'trigger': 'advance', 'source': 'play_again', 'dest': 'input_number', 'unless':'is_ready_to_move_on'}

                
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
