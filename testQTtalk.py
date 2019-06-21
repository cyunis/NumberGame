import sys
import rospy
from std_msgs.msg import String
rospy.init_node('QTexNode')
#Talk1 = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size = 10)
#Talk1.publish("Guess a number between 1 and 100!") #QT says this


wtime_begin = rospy.get_time()
rospy.loginfo("ready...")
speechSay_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
speechSay_pub.publish("Hello! I am QT!")

print(speechSay_pub.get_num_connections())
rospy.wait_for_service('/qt_robot/behavior/talkText')
#rospy.spin()
