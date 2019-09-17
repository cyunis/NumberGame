import time
import random
import math

class statementRandomizer:
    def __init__(self):
        self.supinateList = [999] #will hold the 10 most recent values for supination
        self.pronateList = [-999] #will hold the 10 most recent values for pronation
        self.performedBehaviors = [[],[],[],[],[],[]]

        self.guessStatements = {
            1: "guess1",
            2: "guess2",
            3: "guess3",
            4: "guess4",
            5: "guess5",
            6: "guess6",
            7: "guess7",
            8: "guess8",
            9: "guess9",
            10: "guess10",
            11: "guess11",
            12: "guess12",
            13: "guess13"
        }

        self.bucket1 = {
            1: "clarify1",
            2: "clarify2",
            3: "clarify3",
            4: "clarify4",
            5: "clarify5",
            6: "clarify6",
            7: "clarify7",
            8: "clarify8",
            9: "clarify9",
            10: "clarify10",
            11: "clarify11",
            12: "clarify12",
            13: "clarify13"
        }


        self.bucket2 = {
            1: "encourage1",
            2: "encourage2",
            3: "encourage3",
            4: "encourage4",
            5: "encourage5",
            6: "encourage6",
            7: "encourage7",
            8: "encourage8",
            9: "encourage9",
            10: "encourage10",
            11: "encourage11",
            12: "encourage12",
            13: "encourage13"
        }

        self.bucket3 = {
            1: "encourageless1",
            2: "encourageless2",
            3: "encourageless3",
            4: "encourageless4",
            5: "encourageless5",
            6: "encourageless6",
            7: "encourageless7",
            8: "encourageless8",
            9: "encourageless9",
            10: "encourageless10",
            11: "encourageless11",
            12: "encourageless12",
            13: "encourageless13"
        }

        self.bucket4 = {
            1: "rewardless1",
            2: "rewardless2",
            3: "rewardless3",
            4: "rewardless4",
            5: "rewardless5",
            6: "rewardless6",
            7: "rewardless7",
            8: "rewardless8",
            9: "rewardless9",
            10: "rewardless10",
            11: "rewardless11",
            12: "rewardless12",
            13: "rewardless13"
        }

        self.bucket5 = {
            1: "reward1",
            2: "reward2",
            3: "reward3",
            4: "reward4",
            5: "reward5",
            6: "reward6",
            7: "reward7",
            8: "reward8",
            9: "reward9",
            10: "reward10",
            11: "reward11",
            12: "reward12",
            13: "reward13"
        }

    def chooseRandomStatement(self, statementType):
        mapping = {
            0: self.guessStatements,
            1: self.bucket1,
            2: self.bucket2,
            3: self.bucket3,
            4: self.bucket4,
            5: self.bucket5
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
    GAS_time_scores = [5, 4, 3, 2, 1] # are these upper bounds on the ranges?? (also get these from the global values)

    for index in range(len(GAS_time_scores)):
        if gesture_time > GAS_time_scores[index]:
            return index
    #if we get here, the thumb angle is higher than the highest GAS score
    return len(GAS_time_scores)

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
