import sys
import rospy
from cordial_core import RobotManager
from std_msgs.msg import String

letters = ['A','B','C','D','E','F','G','H','I','J','K','L']

rospy.init_node('QTexNode')
#Talk1 = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size = 10)
#Talk1.publish("Guess a number between 1 and 100!") #QT says this

rm = RobotManager("DB1")

# for i in range(4):
#     rm.say("intro"+str(i+1), wait=True)

# rm.say("startgame")

# for i in range(3):
#     rm.say("another"+str(i+1) , wait=True)

for i in range(12):
    rm.say("clarify"+letters[i], wait=True)

for i in range(12):
    rm.say("encourage"+letters[i], wait=True)

for i in range(12):
    rm.say("encourageless"+letters[i], wait=True)

for i in range(12):
    rm.say("rewardless"+letters[i], wait=True)

for i in range(12):
    rm.say("reward"+letters[i], wait=True)

for i in range(8):
    for j in range(3):
        k = i*3 #which part of 50 set 
        rm.say("guess"+letters[i]+str(j+k), wait=True) 

for i in range(9):
    for j in range(3):
        k = i*3 #which part of 50 set 
        rm.say("second"+letters[i]+str(j+k+20), wait=True)

rm.say("secondB47")
rm.say("guessH48")
rm.say("guessD49")
rm.say("secondI50")
rm.say("endgame")
