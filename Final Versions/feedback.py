import time
import random
import math

class statementRandomizer:
    def __init__(self):
        self.supinateList = [999] #will hold the 10 most recent values for supination
        self.pronateList = [-999] #will hold the 10 most recent values for pronation
        self.performedBehaviors = [[],[],[],[],[],[],[]]

        self.guessStatements = {
            1: "guessB",
            2: "guessC",
            3: "guessD",
            4: "guessE",
            5: "guessF",
            6: "guessG",
            7: "guessH",
            8: "guessI"
        }
        
        self.higher_lower_statements = {
            1: "secondB",
            2: "secondC",
            3: "secondD",
            4: "secondE",
            5: "secondF",
            6: "secondG",
            7: "secondH",
            8: "secondI",
            9: "secondJ",

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
            11: "clarifyK"
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
            11: "encourageK"
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
            11: "encouragelessK"
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
            11: "rewardlessK"
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
            11: "rewardK"
        }

    def chooseRandomStatement(self, statementType):
        mapping = {
            0: self.guessStatements,
            1: self.bucket1,
            2: self.bucket2,
            3: self.bucket3,
            4: self.bucket4,
            5: self.bucket5,
            6: self.higher_lower_statements
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
