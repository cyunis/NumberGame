import time
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
    def __init__(self, ):

        rospy.init_node('logger_node')

        self.gesture_sub = rospy.Subscriber('/qt_robot/gesture/play', String, self.callback)
        self.audio_play_sub = rospy.Subscriber('/qt_robot/audio/play', String, self.callback2)

    def callback(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

    def callback2(self, msg):
        print('time: {}, command: {}'.format(datetime.utcnow(), msg.data))

logger = Logger()
while(1):
    pass
# rospy.spin()