import time
import os
import csv
import logging
import io

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
        
        def setup_logger(name, log_file, level=logging.INFO):
            """Function setup as many loggers as you want"""
            formatter = logging.Formatter('%(message)s') # Just print the string to the file, nothing else

            handler = logging.FileHandler(log_file)        
            handler.setFormatter(formatter)

            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)

            return logger

        rospy.init_node('logger_node')

        path = '/home/qtrobot/Documents/'
        try:
            os.mkdir(path + ID)
        except Exception as e:
            print(e)
        

        self.game_data_file = setup_logger('game_data_logger', path + ID + '/' + 'game_data_logfile.csv') #csv.writer(open('game_data.csv', 'w'))
        self.game_data_file.info('start time, time, beaglebone time, previous state, current state, game aborted?, orthosis malfunction?')

        self.game_metadata_file = setup_logger('game_meta_data_logger',  path + ID + '/' + 'game_meta_data.csv') #csv.writer(open('game_metadata.csv', 'w'))
        self.game_metadata_file.info('start time, time, beaglebone time, total yes, total no, total incorrect answers, total orthosis mistakes, <BUCKETS FILL IN HERE>')

        self.thumb_data_file = setup_logger('game_data_logger', path + ID + '/' + 'thumb_data_logfile.csv')
        self.thumb_data_file.info('start time\ttime\tbeaglebone time\tthumb data\tcollection conditions')#GAS bucket for angle, GAS bucket for time')

        self.robot_data_file = setup_logger('game_data_logger', path + ID + '/' + 'robot_data_logfile.csv')
        self.robot_data_file.info('start time, time, beaglebone time, history of angle performance, history of time performance, gesture key, statement key')

        self.gamedata_sub = rospy.Subscriber('/logging/gamedata', String, self.log_game_data)
        self.gamemetadata_sub = rospy.Subscriber('/logging/gamemetadata', String, self.log_game_metadata)
        self.thumbdata_sub = rospy.Subscriber('/logging/thumbdata', String, self.log_thumb_data)
        self.robotdata_sub = rospy.Subscriber('/logging/robotdata', String, self.log_robot_data)

    def log_game_data(self, msg):
        print(str(msg.data))
        self.game_data_file.info(str(msg.data))

    def log_game_metadata(self, msg):
        self.game_metadata_file.info(str(msg.data))

    def log_thumb_data(self, msg):
        self.thumb_data_file.info(str(msg.data))

    def log_robot_data(self, msg):
        self.robot_data_file.info(str(msg.data))
        
    #def exit(self):
        
logger_node = Logger('Participant_11test11')

while(1):
    rospy.spin()
