import transitions
import time
import re
from transitions.extensions import GraphMachine as Machine
from feedback import statementRandomizer
#from logger import Logger
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
import signal

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(game.start_time, time.time(), game.bb_time, game.number_of_supinations, game.number_of_pronations, game.wrong_counter, game.orthosis_mistake)
        game.gamemetadata_pub.publish(data)
        print(data)
        print('The game metadata have been logged and now the game will terminate :3')

        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


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
        
        self.gamedata_pub = rospy.Publisher('/logging/gamedata', String, queue_size=5)
        self.gamemetadata_pub = rospy.Publisher('/logging/gamemetadata', String, queue_size=5)
        self.thumbdata_pub = rospy.Publisher('/logging/thumbdata', String, queue_size=5)
        self.robotdata_pub = rospy.Publisher('/logging/robotdata', String, queue_size=5)
        
        #subscribers
        self.thumb_sub = rospy.Subscriber("/thumb_result", String, self.process_thumb_data)
        self.beaglebone_sub = rospy.Subscriber("/openwearable_new", String, self.process_beaglebone_data)

        #data to measure
        self.start_time = time.time()
        self.bb_time = -1
        self.number_of_completed_games = 0
        self.number_of_supinations = 0 #yes
        self.number_of_pronations = 0 #no
        self.incorrect_orthosis_behavior = False
        self.wrong_counter = 0
        self.orthosis_mistake = 0
        self.isLeftHanded = False

        self.recording_start_time = self.start_time
        self.gesture_values = []

        self.average_thumb_value = 1
        self.gesture_time = 3.2 #seconds, use GAS1 value

        with open("/home/qtrobot/calibration.txt",'r') as calib_file:
            line = calib_file.readline()
            self.avg_a = float(line.split('~')[1])
            self.avg_down_a = float(line.split('~')[3])
        self.supinate_angle = .8*self.avg_a #degrees, use GAS1 value
        self.pronate_angle = .8*self.avg_down_a #degrees, use GAS1 value
        self.thumb_time = 5 #seconds
        
        #data to make game run smoothly
        self.statementRandomizer = statementRandomizer()
        self.robotManager = RobotManager('DB1')
        
        self.use_robot = use_qt_robot
        self.ready_to_begin = False
        self.guess_lower_bound = 1
        self.guess_upper_bound = 50
        self.guesses = []
        self.number = 0
        self.ready_to_move_on = False
        self.is_aborted = False
        self.prev_state = None
        
        self.nointro = False
        self.choice_condition = False 
        self.computer_true = False
       
        

    #callback functions
    def process_thumb_data(self, msg):
    
        if(self.start_recording == True):
            #save the previous recording
            data = '{}\t{}\t{}\t{}\t{}\t{}'.format(self.start_time, self.recording_start_time, time.time(), self.bb_time, self.gesture_values,'resting values')
            self.thumbdata_pub.publish(data)
            self.gesture_values = []
            self.start_recording = False
            self.recording_start_time = time.time()

        data = str(msg.data)
        data_list = data.split('+')
        thumb_status = int(data_list[0]) # -1->thumbs down, 0->horizontal 1->thumbs up 
        thumb_angle = float(data_list[1]) # angle between 
        
        if(self.isLeftHanded == True):
            thumb_angle = -(thumb_angle - 180)
        #read the button values to see if the green button is pressed -> orthosis_mistake += 1
        self.gesture_values.append({'time': time.time() - self.recording_start_time, 'angle': thumb_angle})


    def process_beaglebone_data(self, msg): 
        
        strdata = str(msg.data)
        vals = re.split(r'\t+', strdata)
        # split data into useful parts
        #val = strdata.split('\\t')
        #val = val[0].split('\\t')
        #temp = val[0].split('\\t')
        
        time_bb = int(vals[0])
        sync = int(vals[1])
        button_value = int(vals[2])

        #the code below should be a separate function for aborting
        if(button_value == -1):
            self.robotManager.stop_speech()
            self.is_aborted = True
            self.abort()
            
        if(button_value == 1):
            self.incorrect_orthosis_behavior = True
            
        if(sync == 1):
            self.ready_to_begin = True
            
        self.bb_time = time_bb


    #helper functions to make sure that transitions are executed correctly
    def is_ready_to_move_on(self):
        #return whether or not the state machine can continue
        return self.ready_to_move_on

    def skip_intro(self):
        #return if there should be no intro
        return self.nointro


    def check_state_machine_status(self):
        if(self.is_aborted):
            raise ValueError('I should not be here')


    def reset_ready_to_move_on(self):
        self.play_gesture(8) #do small gestures at each transition ~= all the time
        #called after every transition is completed
        
        self.ready_to_move_on = False
        self.prev_state = self.state
        


    def guess_equals_number(self):
        return self.guesses[-1] == self.number

    def play_gesture(self, gesture_index, params='None'):
        if(self.use_robot):
            gesture_name = self.statementRandomizer.chooseRandomStatement(gesture_index)
            gesture_data='{}\t{}\t{}\t{}\t{}\t{}'.format(self.start_time, time.time(), self.bb_time, 'gesture', gesture_name, params)
            self.robotdata_pub.publish(gesture_data)
            
            print('playing gesture: {}'.format(gesture_name))
            if(gesture_name.startswith('gestures_programmed')):
                self.gestures_programmed(int(gesture_name.split('(')[1].split(')')[0]))
            else:
                self.gesture_pub.publish(gesture_name)


    def give_feedback(self):
        if(self.use_robot):
            tag = self.statementRandomizer.getResponseBehavior(self.average_thumb_value, self.gesture_time)
            performance_parameters = {'supinate_history': self.statementRandomizer.supinateList, 'pronate_history': self.statementRandomizer.pronateList, 'angle_value':self.average_thumb_value, 'time_value':self.gesture_time }
            print(tag)
            self.play_gesture(12)
            self.cordial_say(tag, wait=True, params=performance_parameters)
        else:
            #say the computer screen thingy
            tag = self.statementRandomizer.chooseRandomStatement(13)
            performance_parameters = {'supinate_history': self.statementRandomizer.supinateList, 'pronate_history': self.statementRandomizer.pronateList, 'angle_value':self.average_thumb_value, 'time_value':self.gesture_time }
            self.cordial_say(tag, wait=True, params=performance_parameters)

    def cordial_say(self, tag, wait=False, params='None'):
        speech_data='{}\t{}\t{}\t{}\t{}\t{}'.format(self.start_time, time.time(), self.bb_time, 'speech', tag, params)
        self.robotdata_pub.publish(speech_data)

        self.robotManager.say(tag, wait=wait)


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
        
        data = '{}\t{}\t{}\t{}\t{}\t{}'.format(self.start_time, self.recording_start_time, time.time(), self.bb_time, self.gesture_values,'measured trial')
        self.thumbdata_pub.publish(data)
        self.gesture_values = []
        self.start_recording = False
        self.recording_start_time = time.time()
        
        self.play_gesture(11) #do gestures while waiting for answer
    
        num_above_thresh = 0
        supinate_angle_sum = 0 #yes
        num_below_thresh = 0
        pronate_angle_sum = 0 #no

        #check to see if the gesture passes the threshold for normal GAS score
        for value in values:
            if value['angle'] > self.supinate_angle:
                supinate_angle_sum += value['angle']
                num_above_thresh += 1
            elif value['angle'] < self.pronate_angle:
                pronate_angle_sum += value['angle']
                num_below_thresh += 1

        if(num_below_thresh == 0 and num_above_thresh == 0):
            angle = 0
            timeontask = 1
        elif( num_below_thresh < num_above_thresh):
            angle = supinate_angle_sum / num_above_thresh
            timeontask = (num_above_thresh * duration) / len(values)
        else:
            angle = pronate_angle_sum / num_below_thresh
            timeontask = (num_below_thresh * duration) / len(values)

        self.average_thumb_value = angle
        self.gesture_time = timeontask

        if(self.average_thumb_value > self.supinate_angle and self.incorrect_orthosis_behavior == False):
            self.number_of_supinations += 1
        if(self.average_thumb_value < self.pronate_angle and self.incorrect_orthosis_behavior == False):
            self.number_of_pronations += 1

        print('angle: {}, time: {}'.format(self.average_thumb_value, self.gesture_time))

    def more_instruction(self):
        print('giving more instructions')
        self.play_gesture(10)
        self.cordial_say('intro5', wait=True)

    #logic for each state transition
    def get_name(self):
        self.play_gesture(10)
        if(self.computer_true):
            self.cordial_say('intro1comp', wait=True)
        else:
            self.cordial_say('intro1qt', wait=True)
        self.name = raw_input('What is their name?')


    def give_instruction(self):
        #give instruction to the game
        self.cordial_say('intro2', wait=True)
        print('you will play a simple thumbs up/down game with me!')


    def on_enter_practice_thumb_up(self):
        self.check_state_machine_status()
        #ask to demonstrate a thumbs up
        self.play_gesture(10)
        self.cordial_say('intro3', wait=True)
        print('practice thumb up')
        self.get_thumb_data(self.thumb_time)
        print(self.average_thumb_value, self.gesture_time)
        self.ready_to_move_on = self.average_thumb_value > 0


    def practice_doesnt_go_up(self):
        #ask to try thumbs up again
        self.play_gesture(8) #small gestures for clarify
        self.cordial_say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        self.wrong_counter += 1
        print('try to put your thumb up again')


    def on_enter_practice_thumb_down(self):
        self.check_state_machine_status()
        #ask for a thumbs down
        self.play_gesture(10)
        self.cordial_say('intro4', wait=True)
        print('practicing thumb down')
        self.get_thumb_data(self.thumb_time)
        self.ready_to_move_on = self.average_thumb_value < 0


    def practice_doesnt_go_down(self):
        #ask to try to put a thumbs down again
        self.play_gesture(8) #small gestures for clarify
        self.cordial_say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True) #should have a condition to check for yes/no with different feedback sentences
        self.wrong_counter += 1
        print('try to put your thumb down again')


    def on_enter_input_number(self):
        #"secretly" input the number
        self.play_gesture(10)
        
        self.cordial_say('startgame', wait=True)
        self.check_state_machine_status()
        self.number = input('What is the number being guessed?')


    def calculate_guess(self):
        half_range = int((self.guess_upper_bound - self.guess_lower_bound)/2)
        ideal_guess = half_range+ self.guess_lower_bound
        guess = ideal_guess + random.randint(-half_range, half_range)
        while(guess in self.guesses):
            guess = ideal_guess + random.randint(-half_range, half_range)
        self.guesses.append(guess)
        print('guess list is: '+str(self.guesses))


    def on_enter_make_guess(self):
        self.check_state_machine_status()

        #ask if the guessed number is correct
        self.play_gesture(9)
        statement_key = self.statementRandomizer.chooseRandomStatement(0)
        self.cordial_say(statement_key+ '{}'.format(self.guesses[-1]), wait=True)
        modifier = 1 if statement_key[-1] in ['A', 'B', 'C', 'D'] else -1
        #get the angle measurements from the camera
        self.get_thumb_data(self.thumb_time)

        self.ready_to_move_on = modifier * self.average_thumb_value > 0


    def incorrect_guess_response(self):
        #try asking again
        self.play_gesture(8) #small gestures for clarify
        self.cordial_say(self.statementRandomizer.chooseRandomStatement(1, self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        self.wrong_counter += 1
        print('actually, let me ask in a different way...')


    def on_enter_higher_or_lower(self):
        self.check_state_machine_status()
        #ask if number is higher than the guess
        self.play_gesture(9)
        statement_key = self.statementRandomizer.chooseRandomStatement(6)
        self.cordial_say( statement_key + '{}'.format(self.guesses[-1]), wait=True)

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
        self.wrong_counter += 1
        self.cordial_say(self.statementRandomizer.chooseRandomStatement(1,self.average_thumb_value), wait=True)  #should have a condition to check for yes/no with different feedback sentences
        print('hmmmm are you sure?')


    def on_enter_play_again(self):
        self.check_state_machine_status()

        #say that QT won
        if(self.choice_condition):
            self.cordial_say('anotherchoice', wait=True)
            data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.start_time, time.time(), self.bb_time, self.number_of_supinations, self.number_of_pronations, self.wrong_counter, self.orthosis_mistake)
            self.gamemetadata_pub.publish(data)
            sys.exit()
            

        else:    
            self.play_gesture(12)
            self.cordial_say(self.statementRandomizer.chooseRandomStatement(7), wait=True)

            print(self.statementRandomizer.performedBehaviors)
            self.get_thumb_data(self.thumb_time)
            # res = input('woohoo I won, want to play again?')
            
            data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.start_time, time.time(), self.bb_time, self.number_of_supinations, self.number_of_pronations, self.wrong_counter, self.orthosis_mistake)
            self.gamemetadata_pub.publish(data)

            self.number_of_completed_games += 1
            self.guesses = []
            self.guess_lower_bound = 1
            self.guess_upper_bound = 50
            self.start_time = time.time()
            self.ready_to_move_on = self.average_thumb_value < 0


    def on_enter_end(self):
        #add the gesture for bye bye
        data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.start_time, time.time(), self.bb_time, self.number_of_supinations, self.number_of_pronations, self.wrong_counter, self.orthosis_mistake)
        self.gamemetadata_pub.publish(data)

        self.cordial_say('endgame')
        print('thanks for playing!')
        print('stats: games played: {}\ntime played: {}'.format(self.number_of_completed_games, time.time()-self.start_time))
        sys.exit()
        
    def log_game_data(self):
        data = "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.start_time, time.time(), self.bb_time, self.prev_state, self.state, self.is_aborted, self.incorrect_orthosis_behavior)
        self.gamedata_pub.publish(data) 
        
        if(self.incorrect_orthosis_behavior):
            self.orthosis_mistake += 1
            self.incorrect_orthosis_behavior = False


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


states = ['get_name', 'practice_thumb_up', 'practice_thumb_down', 'input_number', 'make_guess', 'higher_or_lower', 'play_again', 'end', 'skip_intro']
transitions = [
                { 'trigger':'abort', 'source':'*', 'dest':'end'}, #all states go to the end if the button is pressed
                
                { 'trigger': 'advance', 'source': 'get_name', 'dest': 'practice_thumb_up', 'prepare':'get_name', 'before':'give_instruction'},

                { 'trigger': 'advance', 'source': 'practice_thumb_up', 'dest': 'practice_thumb_down', 'conditions':'is_ready_to_move_on' },
                { 'trigger': 'advance', 'source': 'practice_thumb_up', 'dest': 'practice_thumb_up', 'unless':'is_ready_to_move_on', 'before':'practice_doesnt_go_up'},

                { 'trigger': 'advance', 'source': 'practice_thumb_down', 'dest': 'input_number', 'conditions':'is_ready_to_move_on', 'before':'more_instruction' },
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

                { 'trigger': 'advance', 'source': 'skip_intro', 'dest': 'input_number'},
            ]

game = NumberGameInteraction(False)
start_state = 'skip_intro' if game.nointro == True else 'get_name'
machine = Machine(model=game, states=states, transitions=transitions, initial=start_state, before_state_change='reset_ready_to_move_on', after_state_change='log_game_data', show_state_attributes=True, show_conditions=True)
game.get_graph().draw('TommyThumbDiagram.png', prog='dot')

while(not game.ready_to_begin):
    print(game.ready_to_begin)
    rospy.sleep(0.1)

while(1):
    print(game.state)
    print('to')
    game.advance()
    print(game.state)
    print('---------')
