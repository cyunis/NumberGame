import time
import random
import math

class feedbackController:
    def __init__(self):
        self.supinateList = []
        self.pronateList = []
        self.performedBehaviors = [[],[],[],[],[]]

        self.bucket1 = {
            1: "clarify1",
            2: "clarify2"
        }


        self.bucket2 = {
            1: "encourage1",
            2: "encourage2",
            3: "encourage3",
            4: "encourage4"
        }

        self.bucket3 = {
            1: "encourageLess1",
            2: "encourageLess2",
            3: "encourageLess3"
        }

        self.bucket4 = {
            1: "rewardLess1",
            2: "rewardLess2",
            3: "rewardLess3",
            4: "rewardLess4",
            5: "rewardLess5"
        }

        self.bucket5 = {
            1: "reward1",
            2: "reward2"
        }

    def chooseRandom(self, bucketNumber):
        upperBound = 0
        behaviorDict = {}

        if(bucketNumber == 1):
            upperBound = len(self.bucket1.keys())
            behaviorDict = self.bucket1
        if(bucketNumber == 2):
            upperBound = len(self.bucket2.keys())
            behaviorDict = self.bucket2
        if(bucketNumber == 3):
            upperBound = len(self.bucket3.keys())
            behaviorDict = self.bucket3
        if(bucketNumber == 4):
            upperBound = len(self.bucket4.keys())
            behaviorDict = self.bucket4
        if(bucketNumber == 5):
            upperBound = len(self.bucket5.keys())
            behaviorDict = self.bucket5

        if(upperBound == len(self.performedBehaviors[bucketNumber - 1])):
            self.performedBehaviors[bucketNumber - 1] = []

        behaviorNumber = random.randint(1,upperBound)
        while(behaviorNumber in self.performedBehaviors[bucketNumber-1]):
            behaviorNumber = random.randint(1,upperBound)

        self.performedBehaviors[bucketNumber-1].append(behaviorNumber)
        return behaviorDict[behaviorNumber]


    def getBehavior(self, thumb_angle, gesture_time):
        supinate = True
        pronate = False

        if(supinate):
            appendValue(self.supinateList, thumb_angle)
        elif(pronate):
            appendValue(self.pronateList, thumb_angle)
        else:
            print('Uh-Oh, that is neither supinate nor pronate')

        #current angle is the best seen so far
        if(pronate and max(self.pronateList) == thumb_angle) or (supinate and min(self.supinateList) == thumb_angle):
            behavior = self.chooseRandom(5) #maybe we want a seperate set of improved behaviors?

        #make the buckets based on the GAS variables
        angle_bucket = determine_angle_GAS_bucket(thumb_angle)
        time_bucket = determine_time_GAS_bucket(gesture_time)
        print('angle bucket is {}, time bucket is {}'.format(angle_bucket, time_bucket))
        case = int(math.ceil((angle_bucket + time_bucket) / 2))

        #return the behavior key
        return self.chooseRandom(case)


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
            return index + 1
    #if we get here, the thumb angle is higher than the highest GAS score
    return len(GAS_angle_scores)

def determine_time_GAS_bucket(gesture_time):
    #TODO: get these from a file!!!
    GAS_time_scores = [5, 4, 3, 2, 1] # are these upper bounds on the ranges?? (also get these from the global values)

    for index in range(len(GAS_time_scores)):
        if gesture_time > GAS_time_scores[index]:
            return index + 1
    #if we get here, the thumb angle is higher than the highest GAS score
    return len(GAS_time_scores)




# fb = feedbackController()
# start_time = time.time()
#
# while 1:
#     thumb_angle = random.randint(1,60)
#     gesture_time = random.randint(1,50)*0.1
#
#     print('angle: {}, time: {}'.format(thumb_angle, gesture_time))
#
#     fb.getBehavior(thumb_angle, gesture_time, time.time() - start_time, 'nathan')
#     for i in range(1,6):
#         print('Bucket{}: {}'.format(i, fb.performedBehaviors[i-1]))
