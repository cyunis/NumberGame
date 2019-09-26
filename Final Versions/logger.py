import time
import os
import csv
from feedback import statementRandomizer
from std_msgs.msg import String
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from datetime import datetime
import roslib; roslib.load_manifest('cordial_example')
import rospy
from cordial_core import RobotManager

class Logger:
    def __init__(self, ID):

        rospy.init_node('logger_node')

        path = '~/Documents'
        try:
            os.mkdir(path + '/' + ID)
        except Error as e:
            print(e)

        self.game_data_file = csv.writer(open(ID + '/game_data.csv', 'w'))
        self.game_data_file.writerow(['start time', 'time', 'current state', 'next state', 'ready_to_move_on', 'game aborted?', 'orthosis malfunction?'])

        self.game_metadata_file = csv.writer(open(ID + '/game_metadata.csv', 'w'))
        self.game_metadata_file.writerow(['start time', 'time', 'total supinations', 'total pronations', 'length', 'bucket angle definitions', 'bucket time definitions'])

        self.thumb_data_file = csv.writer(open(ID + '/thumb_data.csv', 'w'))
        self.thumb_data_file.writerow(['start time', 'time', 'thumb data', 'GAS bucket for angle', 'GAS bucket for time'])

        self.robot_data_file = csv.writer(open(ID + '/robot_data.csv', 'w'))
        self.robot_data_file.writerow(['start time', 'time', 'history of angle performance', 'history of time performance', 'gesture key', 'statement key'])

        self.gamedata_sub = rospy.Subscriber('/logging/gamedata', String, self.log_game_data)
        self.gamemetadata_sub = rospy.Subscriber('/logging/gamemetadata', String, self.log_game_metadata)
        self.thumbdata_sub = rospy.Subscriber('/logging/thumbdata', String, self.log_thumb_data)
        self.robotdata_sub = rospy.Subscriber('/logging/robotdata', String, self.log_robot_data)

    def log_game_data(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

    def log_game_metadata(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

    def log_game_metadata(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

    def log_game_metadata(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

logger = Logger()

while(1):
    pass
# rospy.spin()