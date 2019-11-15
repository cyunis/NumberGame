#!/usr/bin/env python
# encoding=utf8

import sys
import rospy
from cordial_core import RobotManager
from std_msgs.msg import String


rospy.init_node('wiggins')

rm = RobotManager("DB1")
rospy.sleep(2)

#rm.say("wiggins", wait=True)
rm.say("wigginsorthosis", wait=True)
rm.say("bad", wait=True)
raw_input('next')
rm.say("good", wait=True)
raw_input('next')
rm.say("notfriendly", wait=True)
raw_input('next')
rm.say("friendly", wait=True)
raw_input('next')
rm.say("cold", wait=True)
raw_input('next')
rm.say("warm", wait=True)
raw_input('next')
rm.say("unpleasant", wait=True)
raw_input('next')
rm.say("pleasant", wait=True)
raw_input('next')
rm.say("cruel", wait=True)
raw_input('next')
rm.say("kind", wait=True)
raw_input('next')
rm.say("harsh", wait=True)
raw_input('next')
rm.say("sweet", wait=True)
raw_input('next')
rm.say("useful", wait=True)
raw_input('next')
rm.say("valuable", wait=True)
raw_input('next')
rm.say("helpful", wait=True)
raw_input('next')
rm.say("skillful", wait=True)
raw_input('next')
rm.say("clever", wait=True)
raw_input('next')
rm.say("intelligent", wait=True)
raw_input('next')
rm.say("smart", wait=True)

