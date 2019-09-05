#feedback function
def feedback_function(thumb_angle, gesture_time, time, name):
    global speechSay_pub, encourage_dict, reward_dict, clarify_dict, feedback_dict, count, wrongcounter, supinate, pronate
    #give each item weights and combine weights to make a %
    #want reward to be 80-50% and encourage >80% always
    #camera angle, GAS (fatigue), history of gestures, # of prompts
    #camera angles should be matched to buckets on the GAS - need to see lit if standard #s for this (10% is 1, 20% is 2)
        #these should be the most important factors to weight
    #increase the encouragement when GAS, camera angle is worse and increase more if history shows a pattern of worsening    
    #if high number of rewards maybe dont need to increase encouragement as much
    #if a lot of clarification is needed, and bad history of gestures, more encouragement and more reward for lower GAS
    #if history of gestures is bad but shows one good case give a reward
    #history categories: 1)90% good and then 10% bad(sudden dip) 2)equal mixture of good or bad 3)no improvement 4)getting worse 5)getting better 6)90% bad then good
    #1, 3, 4 - more encouragement. 2 - varied encouragement (maybe getting bored?). 5, 6 - more reward + encouragement.
    #1, 6 - high weights.
    #prompt categories: 1)a lot of clarification 2)a little clarification 3)less encouragement than normal 4)a lot of reward 5)a little reward
    #1 - more encouragement (maybe tired?). 2 - more reward. 3 - varied encouragement.
    
    #make the buckets based on the GAS variables
    gestureis = 0
    #if thumb_angle <
    
    #split thumb_angle into pronation or supination
    if thumb_angle>0:
        supinate = thumb_angle #thumbs up
    if thumb_angle<0:
        pronate = thumb_angle #thumbs down
    #gesture_time should be set to reses.count(1) or .count(-1) for supination or pronation respectively
    
    #categorize the gesture into a bucket based on supinate, pronate, gesture_time, time, etc
    
    feedback_dict[count] = [supinate,pronate,gesture_time,time]
    print(feedback_dict)
    count += 1
    #make sure the encouragement plays when it should - include graded cueing? (feedback @ failure) see stroke lit for affectiveness/optimal challenge
    #50 degrees is the threshold, determined by GAS
    if abs(thumb_angle) < 50:
        encourage_prob = 0.85 -abs(thumb_angle/100.0) + time/300.0 #smaller angle, worse performance/ longer time, more tired, more enc
        print("Encouragement prob: " + str(encourage_prob))
        if encourage_prob<0:
            print("Error: encourage_prob is 0!")
            encourage_prob = 0
        if encourage_prob>1:
            print("Error: encourage_prob is 1!")
            encourage_prob = 1
        enc_flag = random.randrange(1,100)
        if enc_flag<encourage_prob*100:
            random_encourage = random.randrange(1,len(encourage_dict))
            speechSay_pub.publish(encourage_dict[random_encourage].format(name))
            print(encourage_dict[random_encourage].format(name))            
    #make sure the reward functions to be only at intermittant intervals - should be v selective
    else:
        for i in range(1, count-1):
            avg_angle += feedback_dict[i][0]
        avg_angle /= (count-2)
        reward_compare = feedback_dict[count-1][0]/avg_angle
        reward_current = 0.5 + abs(thumb_angle/100.0) + time/300.0 #larger angle, better performance/ longer the time playing, more reward
        if reward_compare>reward_current:
            reward_prob = reward_compare
        if reward_current>reward_compare and reward_compare>0.9: #0.9 is the ratio of how much decline between GAS scores (-10%)
            reward_prob = reward_current
        if reward_current>reward_compare:
            reward_prob = 0.5
        if reward_prob<0:
            print("Error: reward_prob is 0!")
            reward_prob = 0
        if reward_prob>1:
            print("Error: reward_prob is 1!")
            reward_prob = 1
        rew_flag = random.randrange(1,100)
        if rew_flag<reward_prob*100 and wrongcounter<10:
            random_rew = random.randrange(1,len(reward_dict))
            speechSay_pub.publish(reward_dict[random_rew].format(name))
            print(reward_dict[random_rew].format(name))
#        if wrongcounter>10:
#            random_clar = random.randrange(1,len(clarify_dict))
#            speechSay_pub.publish(clarify_dict[random_clar].format(name))