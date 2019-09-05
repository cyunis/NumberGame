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
    bucket = determine_GAS_bucket(thumb_angle, gesture_time)
    
    historical_case = get_historical_case(bucket)
    
    # switch between historical cases to determine the increase / decrease
    
    timeScale = log(time) # get some reasonable quantification of the time
    
    #calculate the probability of different feedback
    feedback_probability = timescale * CONSTANT + bucket * CONSTANT + CONSTANT
    
    #grab the specific behavior with the given probability
    
    #play the behavior
    
    
    
    
    
    
    
def determine_GAS_bucket(thumb_angle, gesture_time):
    #place the GAS variables in an array and then find the index at which some combo of the thumb and time lies
    #history depends on the actual angle not the GAS score
    #do we want a seperate set of buckets for each time and angle ?? YES
        #if so, how should we handle the "history case" later for things like they have been getting better at the angle, but the time is worse?
    
    GAS_scores = [10, 20, 30, 40, 50] # are these upper bounds on the ranges?? (also get these from the global values)
    
    for index in range(len(GAS_scores)):
        if thumb_angle < GAS_scores[index]:
            return index
            
    #if we get here, the thumb angle is higher than the highest GAS score        
    return len(GAS_scores)
    
def get_historical_case(bucket)
    #do we want this to be based on the bucket? or is it based on the raw thumb angles? or should it be time? some combo of the two?
    pass
