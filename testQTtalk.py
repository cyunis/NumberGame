import sys
import rospy
from cordial_core import RobotManager
from std_msgs.msg import String

letters = ['A','B','C','D','E','F','G','H','I','J','K','L']

rospy.init_node('QTexNode')
#Talk1 = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size = 10)
#Talk1.publish("Guess a number between 1 and 100!") #QT says this

rm = RobotManager("DB1")

for i in range(4):
    rm.say("intro"+str(i+1))

rm.say("startgame")

for i in range(3):
    rm.say("endgame"+str(i+1))

for i in range(12):
    rm.say("clarify"+letters[i])

for i in range(12):
    rm.say("encourage"+letters[i])

for i in range(12):
    rm.say("encourageless"+letters[i])

for i in range(12):
    rm.say("rewardless"+letters[i])

for i in range(12):
    rm.say("reward"+letters[i])

for i in range(8):
    for j in range(3):
        k = i*3 #which part of 50 set 
        rm.say("guess"+letters[i]+str(j+k)) 

for i in range(9):
    for j in range(3):
        k = i*3 #which part of 50 set 
        rm.say("second"+letters[i]+str(j+k+20))

rm.say("secondB47")
rm.say("guessH48")
rm.say("guessD49")
rm.say("secondI50")