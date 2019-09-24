import time
import random
import math

class statementRandomizer:
    def __init__(self):
        self.supinateList = [999] #will hold the 10 most recent values for supination
        self.pronateList = [-999] #will hold the 10 most recent values for pronation
        self.performedBehaviors = [[],[],[],[],[],[],[],[]]

        self.guessStatements = {
            1: "guessA",
            2: "guessB",
            3: "guessC",
            4: "guessD",
            5: "guessE",
            6: "guessF",
            7: "guessG",
            8: "guessH"
        }
        
        self.higher_lower_statements = {
            1: "secondA",
            2: "secondB",
            3: "secondC",
            4: "secondD",
            5: "secondE",
            6: "secondF",
            7: "secondG",
            8: "secondH",
            9: "secondI",
        }

        self.win_statements = {
            1: "endgame1",
            2: "endgame2",
            3: "endgame3"
        }

        self.bucket1 = {
            1: "clarifyA",
            2: "clarifyB",
            3: "clarifyC",
            4: "clarifyD",
            5: "clarifyE",
            6: "clarifyF",
            7: "clarifyG",
            8: "clarifyH",
            9: "clarifyI",
            10: "clarifyJ",
            11: "clarifyK",
            12: "clarifyL"
        }


        self.bucket2 = {
            1: "encourageA",
            2: "encourageB",
            3: "encourageC",
            4: "encourageD",
            5: "encourageE",
            6: "encourageF",
            7: "encourageG",
            8: "encourageH",
            9: "encourageI",
            10: "encourageJ",
            11: "encourageK",
            12: "encourageL"
        }

        self.bucket3 = {
            1: "encouragelessA",
            2: "encouragelessB",
            3: "encouragelessC",
            4: "encouragelessD",
            5: "encouragelessE",
            6: "encouragelessF",
            7: "encouragelessG",
            8: "encouragelessH",
            9: "encouragelessI",
            10: "encouragelessJ",
            11: "encouragelessK",
            12: "encouragelessL"
        }

        self.bucket4 = {
            1: "rewardlessA",
            2: "rewardlessB",
            3: "rewardlessC",
            4: "rewardlessD",
            5: "rewardlessE",
            6: "rewardlessF",
            7: "rewardlessG",
            8: "rewardlessH",
            9: "rewardlessI",
            10: "rewardlessJ",
            11: "rewardlessK",
            12: "rewardlessL"
        }

        self.bucket5 = {
            1: "rewardA",
            2: "rewardB",
            3: "rewardC",
            4: "rewardD",
            5: "rewardE",
            6: "rewardF",
            7: "rewardG",
            8: "rewardH",
            9: "rewardI",
            10: "rewardJ",
            11: "rewardK",
            12: "rewardL"
        }

    def chooseRandomStatement(self, statementType):
        mapping = {
            0: self.guessStatements,
            1: self.bucket1,
            2: self.bucket2,
            3: self.bucket3,
            4: self.bucket4,
            5: self.bucket5,
            6: self.higher_lower_statements,
            7: self.win_statements
        }
        #convert statement type to actual dictionary
        behaviorDict = mapping[statementType]
        upperBound = len(behaviorDict.keys())

        #clear half of the oldest values from the list of played animations if they have all been played
        if(upperBound == len(self.performedBehaviors[statementType])):
            while len(self.performedBehaviors[statementType]) > upperBound/2:
                self.performedBehaviors[statementType].pop(0)

        #determine the number of the behavior to play, and
        #choose a new behavior if the desired number has already been played
        behaviorNumber = random.randint(1,upperBound)
        while(behaviorNumber in self.performedBehaviors[statementType]):
            behaviorNumber = random.randint(1,upperBound)

        #once the number is found, return the key value for the CoRDial statement
        self.performedBehaviors[statementType].append(behaviorNumber)
        return behaviorDict[behaviorNumber]


    def getResponseBehavior(self, thumb_angle, gesture_time):
        supinate = False
        pronate = True
        rewardOverride = False

        #current angle is the best seen so far
        if(pronate and max(self.pronateList) < thumb_angle) or (supinate and min(self.supinateList) > thumb_angle):
            print('that was the current best in the past  10 runs!')
            rewardOverride = True

        if(pronate and len(self.pronateList) > 3 and self.pronateList[-1] < thumb_angle and self.pronateList[-2] < self.pronateList[-1] and self.pronateList[-3] < self.pronateList[-2]):
            print('that showed improvement over the past three trials')
            rewardOverride = True

        if(supinate and len(self.supinateList) > 3 and self.supinateList[-1] > thumb_angle and self.supinateList[-2] > self.supinateList[-1] and self.supinateList[-3] > self.supinateList[-2]):
            print('that showed improvement over the past three trials')
            rewardOverride = True

        if(supinate):
            appendValue(self.supinateList, thumb_angle)
        elif(pronate):
            appendValue(self.pronateList, thumb_angle)
        else:
            print('Uh-Oh, that is neither supinate nor pronate')

        if rewardOverride:
            return self.chooseRandomStatement(5) #maybe we want a seperate set of improved behaviors?

        #make the buckets based on the GAS variables
        angle_bucket = determine_angle_GAS_bucket(thumb_angle)
        time_bucket = determine_time_GAS_bucket(gesture_time)
        print('angle bucket is {}, time bucket is {}'.format(angle_bucket, time_bucket))
        bucket = int(math.ceil((angle_bucket + time_bucket) / 2))

        #return the behavior key
        return self.chooseRandomStatement(bucket)


def appendValue(listToAppend, valueToAppend):
    maxLength = 10 #parameter that can be tuned
    listToAppend.append(valueToAppend)
    if len(listToAppend) > maxLength:
        listToAppend.pop(0)


def determine_angle_GAS_bucket(thumb_angle):
    #TODO: get these from a file!!!
    GAS_angle_scores = [10, 20, 30, 40, 50] # are these upper bounds on the ranges?? (also get these from the global values)

    for index in range(len(GAS_angle_scores)):
        if thumb_angle < GAS_angle_scores[index]:
            return index
    #if we get here, the thumb angle is higher than the highest GAS score
    return len(GAS_angle_scores)

def determine_time_GAS_bucket(gesture_time):
    #TODO: get these from a file!!!
    GAS_time_scores = [1, 2, 3, 4, 5] # are these upper bounds on the ranges?? (also get these from the global values)

    for index in range(len(GAS_time_scores)):
        if gesture_time < GAS_time_scores[index]:
            return index
    #if we get here, the thumb angle is higher than the highest GAS score
    return len(GAS_time_scores)

# def gestures_programmed(number):
#     if(number == 1):
#         #listening, nod:4s
#         head = Float64MultiArray()
#         head.data = [0,-10]
#         head_pub.publish(head)
#         time.sleep(1)
#         head.data = [0,10]
#         head_pub.publish(head)
#         time.sleep(1)
#         head.data = [0,0]
#         head_pub.publish(head)
#         time.sleep(2)
#     elif(number == 2):
#         #encouragement, hug:6s
#         left_arm = Float64MultiArray()
#         right_arm = Float64MultiArray()
#         left_arm.data = [-20, -10, -15]
#         left_pub.publish(left_arm)
#         right_arm.data = [20, -10, -15]
#         right_pub.publish(right_arm)
#         time.sleep(3)
#         left_arm.data = [90, -60, -30]
#         left_pub.publish(left_arm)
#         right_arm.data = [-90, -60, -30]
#         right_pub.publish(right_arm)
#         time.sleep(3)
#     elif(number == 3):
#         #encouragement, hand clap:8.8s
#         left_arm = Float64MultiArray()
#         right_arm = Float64MultiArray()       
#         left_arm.data = [10, -90, -30]
#         left_pub.publish(left_arm)
#         right_arm.data = [-10, -90, -30]
#         right_pub.publish(right_arm)
#         time.sleep(1.8)
#         left_arm.data = [10, -90, -90]
#         left_pub.publish(left_arm)
#         right_arm.data = [-10, -90, -90]
#         right_pub.publish(right_arm)
#         time.sleep(1)
#         left_arm.data = [10, -90, -30]
#         left_pub.publish(left_arm)
#         right_arm.data = [-10, -90, -30]
#         right_pub.publish(right_arm)
#         time.sleep(1)
#         left_arm.data = [10, -90, -90]
#         left_pub.publish(left_arm)
#         right_arm.data = [-10, -90, -90]
#         right_pub.publish(right_arm)
#         time.sleep(1)
#         left_arm.data = [10, -90, -30]
#         left_pub.publish(left_arm)
#         right_arm.data = [-10, -90, -30]
#         right_pub.publish(right_arm)
#         time.sleep(1)
#         left_arm.data = [90, -60, -30]
#         left_pub.publish(left_arm)
#         right_arm.data = [-90, -60, -30]
#         right_pub.publish(righ0t_arm)
#         time.sleep(3)


# def play_gesture(num):
#     small_gestures = ["numbergame/small1","numbergame/small2","numbergame/small3","numbergame/together","numbergame/together1","numbergame/together2","numbergame/together3","numbergame/head2","numbergame/head3","numbergame/left1","numbergame/left2","numbergame/left3","numbergame/right2","numbergame/right3"]
#     guessing_gestures = ["numbergame/thinking1","numbergame/thinking2","numbergame/thinking3"]
#     talking_gestures = ["numbergame/talking1","numbergame/talking2","numbergame/talking3","numbergame/talking4","numbergame/talking5","numbergame/talking6","QT/challenge"]
#     listening_gestures = ["QT/bored"] #or call gestures_programmed(1)
#     encouragement_gestures = ["QT/surprise","QT/happy"] #or call gestures_programmed(2,3)

#     start = time.time()
#     previous = []
#     b = small_gestures #pick the gesture set you want to play from
#     while i <= num:
#         a = random.randint(1, 1+b)
#         if i>1 and a == previous[i-2] and a != (1+b):
#             previous.append(a+1)
#             a+=1 #increment the value so it doesn't repeat
#         else:
#             previous.append(a)
#         return b[a]
#         #use the publisher for gestures to call the gesture to be played: gesture_pub(b[a])
#         #self.gesturePlay_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
#         if time.time() > start + num:
#             break
#         i = i + 1
#     print("Just did "+str(num)+str(b))

#
# sr = statementRandomizer()
#
# while(1):
#     listID = input('which list?')
#     sr.getResponseBehavior(60 - listID*10, listID)
#     for i in range(0, len(sr.performedBehaviors)):
#         print(sr.performedBehaviors[i])
#
#     print('-------------------------------')
