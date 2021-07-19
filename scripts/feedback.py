import time
import random
import math

class statementRandomizer:
    def __init__(self):
        self.supinateList = [999] #will hold the 10 most recent values for supination
        self.pronateList = [-999] #will hold the 10 most recent values for pronation
        self.performedBehaviors = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.supinate = False
        self.pronate = False

        # with open("/home/qtrobot/calibration.txt",'r') as calib_file:
        #     line = calib_file.readline()
        #     self.avg_a = float(line.split('~')[1])
        #     self.avg_down_a = float(line.split('~')[3])
        #     line = calib_file.readline()
        #     line = calib_file.readline()
        #     self.tot_up = float(line.split('~')[1])
        #     self.tot_down = float(line.split('~')[3])

        self.avg_a = 45
        self.avg_down_a = -45
        self.tot_up = 2
        self.tot_down = 2


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
            9: "secondI"
        }

        self.win_statements = {
            1: "another1",
            2: "another2",
            3: "another3",     
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

        self.small_gestures = {
            1: "numbergame/small1",
            2: "numbergame/small2",
            3: "numbergame/small3",
            4: "numbergame/together",
            5: "numbergame/together1",
            6: "numbergame/together2",
            7: "numbergame/together3",
            8: "numbergame/head2",
            9: "numbergame/head3",
            10: "numbergame/left1",
            11: "numbergame/left2",
            12: "numbergame/left3",
            13: "numbergame/right2",
            14: "numbergame/right3"
        }

        self.guessing_gestures = {
            1: "numbergame/thinking1",
            2: "numbergame/thinking2",
            3: "numbergame/thinking3"
        }

        self.talking_gestures = {
            1: "numbergame/talking1",
            2: "numbergame/talking2",
            3: "numbergame/talking3",
            4: "numbergame/talking4",
            5: "numbergame/talking5",
            6: "numbergame/talking6",
            7: "QT/challenge"
        }
        self.listening_gestures = {
            1: "QT/bored",
            2: "QT/bored",
            3: "QT/bored",
            # 2: "gestures_programmed(1)" #or call gestures_programmed(1)
         } 
        self.encouragement_gestures = {
            1: "QT/surprise",
            2: "QT/happy",
            3: "QT/surprise",
            4: "QT/happy"
            # 3: "gestures_programmed(2)",
            # 4: "gestures_programmed(3)"
         } #or call gestures_programmed(2,3)

        self.wig_ok = {
            1: "fillerA",
            2: "fillerB",
            3: "fillerC",
            4: "fillerD",
            5: "fillerE",
            6: "fillerF",
            7: "fillerG",
            8: "fillerH",
            9: "fillerI",
            10: "fillerJ",
            11: "fillerK",
            12: "fillerL",
            13: "fillerM",
            14: "fillerN",
            15: "fillerO",
            16: "fillerP",
            17: "fillerQ",
            18: "fillerR",
            19: "fillerS",
            20: "fillerT"
        }

    def chooseRandomStatement(self, statementType, angle=0):
        mapping = {
            0: self.guessStatements,
            1: self.bucket1,
            2: self.bucket2,
            3: self.bucket3,
            4: self.bucket4,
            5: self.bucket5,
            6: self.higher_lower_statements,
            7: self.win_statements,
            8: self.small_gestures,
            9: self.guessing_gestures,
            10: self.talking_gestures,
            11: self.listening_gestures,
            12: self.encouragement_gestures,
            13: self.wig_ok
        }

        #convert statement type to actual dictionary
        behaviorDict = mapping[statementType]
        upperBound = len(behaviorDict.keys())
        tries = 0

        #clear half of the oldest values from the list of played animations if they have all been played
        if(upperBound == len(self.performedBehaviors[statementType])):
            while len(self.performedBehaviors[statementType]) > upperBound/2:
                tries += 1
                if tries > 100:
                    print('infinite loop on 225 in feeedback.py')
                self.performedBehaviors[statementType].pop(0)

        #determine the number of the behavior to play, and
        #choose a new behavior if the desired number has already been played
        behaviorNumber = random.randint(1,upperBound)
        while(behaviorNumber in self.performedBehaviors[statementType]):
            tries += 1
            if tries > 100:
                    print('infinite loop on 234 in feedback.py')
            behaviorNumber = random.randint(1,upperBound)

        #once the number is found, return the key value for the CoRDial statement
        self.performedBehaviors[statementType].append(behaviorNumber)
        return behaviorDict[behaviorNumber]


    def getResponseBehavior(self, thumb_angle, gesture_time):
        self.supinate = True if thumb_angle > 0 else False #thumbs up
        self.pronate = True if thumb_angle < 0 else False #thumbs down
        rewardOverride = False

        #current angle is the best seen so far
        if(self.pronate and min(self.pronateList) > thumb_angle) or (self.supinate and max(self.supinateList) < thumb_angle):
            print('that was the current best in the past  10 runs!')
            rewardOverride = True

        if(self.pronate and len(self.pronateList) > 3 and self.pronateList[-1] > thumb_angle and self.pronateList[-2] > self.pronateList[-1] and self.pronateList[-3] > self.pronateList[-2]):
            print('that showed improvement over the past three trials')
            rewardOverride = True

        if(self.supinate and len(self.supinateList) > 3 and self.supinateList[-1] < thumb_angle and self.supinateList[-2] < self.supinateList[-1] and self.supinateList[-3] < self.supinateList[-2]):
            print('that showed improvement over the past three trials')
            rewardOverride = True

        if(self.supinate):
            appendValue(self.supinateList, thumb_angle)
        elif(self.pronate):
            appendValue(self.pronateList, thumb_angle)
        else:
            print('Uh-Oh, that is neither supinate nor pronate')

        if rewardOverride:
            return self.chooseRandomStatement(5) #maybe we want a seperate set of improved behaviors?

        #make the buckets based on the GAS variables
        angle_bucket = self.determine_angle_GAS_bucket(thumb_angle)
        time_bucket = self.determine_time_GAS_bucket(gesture_time, thumb_angle > 0)
        print('angle bucket is {}, time bucket is {}'.format(angle_bucket, time_bucket))
        bucket = int(math.ceil((angle_bucket + time_bucket) / 2.0))

        #return the behavior key
        return self.chooseRandomStatement(bucket)

    def determine_angle_GAS_bucket(self, thumb_angle):
        #TODO: get these from a file!!!
        supinate_scores = [.8*self.avg_a, .9*self.avg_a, self.avg_a, 1.1*self.avg_a, 1.2*self.avg_a]

    # are these upper bounds on the ranges?? (also get these from the global values)
        #import avg_down_a -> multiply by .8, .9, 1, 1.1, 1.2
        pronate_scores = [.8*self.avg_down_a, .9*self.avg_down_a, self.avg_down_a, 1.1*self.avg_down_a, 1.2*self.avg_down_a]



        GAS_angle_scores = []

        if(thumb_angle<0):
            GAS_angle_scores = pronate_scores
        if(thumb_angle>0):
            GAS_angle_scores = supinate_scores

        for index in range(len(GAS_angle_scores)):
            if thumb_angle < GAS_angle_scores[index]:
                return index + 1
        #if we get here, the thumb angle is higher than the highest GAS score
        return len(GAS_angle_scores)

    def determine_time_GAS_bucket(self, gesture_time, supinate):
        #TODO: get these from a file!!!
        
        if supinate:
            tot = self.tot_up
        else:
            tot = self.tot_down

        GAS_time_scores = [.8*tot, .9*tot, tot, 1.1*tot, 1.2*tot] # are these upper bounds on the ranges?? (also get these from the global values)

        for index in range(len(GAS_time_scores)):
            if gesture_time < GAS_time_scores[index]:
                return index + 1
        #if we get here, the thumb angle is higher than the highest GAS score
        return len(GAS_time_scores)


def appendValue(listToAppend, valueToAppend):
    maxLength = 10 #parameter that can be tuned
    listToAppend.append(valueToAppend)
    if len(listToAppend) > maxLength:
        listToAppend.pop(0)

