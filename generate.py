#!/usr/bin/env python
# -*- coding: utf-8 -*-
name = 'Nathan'
hand = 'right'
letters = ['A','B','C','D','E','F','G','H','I','J','K','L']

clarify_dict = {1: 'Sorry {} I didn’t see that, could you repeat that answer for me please?',
    2: "I think that was a yes {}. Could you make a thumbs up again for me please?",
    3: "I think that was a no {}. Could you make a thumbs down again for me please?",
    4: "Could you please show me that answer again {}?",
    5: "Sorry I didn’t see that {}, could you repeat that answer for me please?",
    6: "Hey {} could you please show me that answer again?",
    7: 'I didn’t understand {} I need you to show me again please!',
    8: '{} I didn’t see that can you please show me again!',
    9: 'Was that a thumbs up? Can you show me again please?',
    10: 'Was that a thumbs down? Can you show me again please?',
    11: '{} please show me what you did again I missed it.',
    12: 'Can you show me what you did again please?'} 
#2/3 and 9/10 should be used depending on what the gesture was supposed to be

encourage_dict = {1: 'Good job {}!',
    2: 'That was your best one so far! Keep up the good work {}!',
    3: 'I can tell you are trying really hard {}, nice job!',
    4: 'You are getting better at this {}, wow!',
    5: 'I know this is hard {}, keep trying!',
    6: 'Hooray! Let’s play again {}!',
    7: 'Hey {}, good job!',
    8: 'That was your best one so far {}! Keep up the good work!',
    9: 'Hey {} I can tell you are trying really hard, nice job!',
    10: 'Everyone, {} is getting better at this!',
    11: 'Keep trying, I know this is hard {} but you got it!',
    12: 'Hooray you did great {}!'} 

encourageless_dict = {1: 'That was good {}.',
    2: 'Hey {} keep it up.',
    3: 'Nice job {}.',
    4: 'Hey {} nice job.',
    5: 'Keep it up {}.',
    6: 'You’re doing well {}.',
    7: '{} you’re doing well.',
    8: 'Cool you got it {}.',
    9: '{} you got it.',
    10: 'That was pretty good {}.',
    11: 'That was a good one {}.',
    12: 'Hey {} I can understand you!'}

rewardless_dict = {1: 'You’re good at this {}!',
    2: 'I think {} is great at this game.',
    3: 'You must work your thumbs out {} you’re good!',
    4: 'Yay keep it up {}!',
    5: '{} you made me smile.',
    6: 'I think that {} made one of the best gestures I’ve ever seen!',
    7: 'That was a good gesture!',
    8: '{} is very good at this game.',
    9: 'Keep showing me what you got!',
    10: 'This game is fun to play with you {}.',
    11: 'You are playing well {}!',
    12: 'I want to keep playing with you {}!'}

reward_dict = {1: "Let’s party!",
    2: "I have a joke {}, why did a crocodile marry a chicken? Because crock-o-doodle-doodle is a good last name!",
    3: "Who has a thumb and plays really well? {} does!",
    4: "I like playing games with you {}, you’re very fun. Do you like playing with me?",
    5: "Let’s celebrate!",
    6: "I am happy to play games with you {}!",
    7: 'That was the best gesture I’ve seen!',
    8: '{} is the best at this game!',
    9: 'You are playing so well keep it up!',
    10: 'That was a great gesture {}!',
    11: 'You must be a superhero you’re so strong.',
    12: '{} I love playing with you!'} 

guess_dict = {1: 'Is {} right? Please show me a thumbs up or down.',
    2: 'Ok I think I know your number. Is it {}?',
    3: 'Is your number {}? Please show me yes or no.',
    4: 'I guess {}. Did I guess your number?',
    5: 'Am I wrong if I guess {}?',
    6: 'Is {} the wrong guess?',
    7: 'Is {} wrong? Please show me yes or no.',
    8: 'I guess {} am I wrong?'}
#make sure name and number are in the right spot for every phrase - use 0 or 1 in the brackets to call in order
#higher or lower
second_dict = {1: 'Hey {} is your number higher than {}? Show me yes or no.',
    2: 'Oh no, I guessed {1}. Did I guess bigger than your number {0}?',
    3: 'Hmm is {1} bigger than my number {0}?',
    4: 'Hey is your number higher than {1} {0}? Show me yes or no.',
    5: 'Oh no {}, I guessed {}. Did I guess bigger than your number?',
    6: 'Hmm {}, is {} bigger than my number?',
    7: 'Hey is your number higher than {1}? Show me yes or no please {0}.',
    8: 'Oh no, I guessed {1} {0}! Did I guess bigger than your number?',
    9: 'Hmm tell me {} is {} bigger than my number?'} 

f = open("script.txt",mode = 'a',encoding = 'utf-8')

f.writelines('[intro1]'+'Hello, my name is QTRobot. What is your name?\n')
f.writelines('[intro2]'+"Hi "+name+", I would like to play a guessing game with you. In the game, I ask you questions, and you answer yes or no by using a thumbs up or a thumbs down with your "+hand+" hand. Let’s practice.  Can you show me a thumbs up to say yes?\n")
f.writelines('[intro3]'+"Awesome! Now can you show me a thumbs down to say no?\n")
f.writelines('[intro4]'+"Thanks! During the game, please keep your hand flat on the arm rest until I ask you a question. If your thumb is going the wrong way, just push the green button. And just do your best. Can you please show me yes if that’s ok?\n")
f.writelines('[startgame]'+"Let's play now! Please think of a number between 1 and 50.\n")
f.writelines('[endgame1]'+"Hooray I got it! Thanks {} for playing with me. Let’s play again!\n".format(name))
f.writelines('[endgame2]'+"Yay I guessed right! Do you want to play again please?\n")
f.writelines('[endgame3]'+"Woo hoo that was fun! Do you want to play one more game?\n")

for i in clarify_dict.keys():
    f.writelines("[clarify" + letters[i-1] + "]" + clarify_dict[i].format(name)+'\n')

for i in encourage_dict.keys():
    f.writelines("[encourage" + letters[i-1] + "]" + encourage_dict[i].format(name)+'\n')

for i in encourageless_dict.keys():
    f.writelines("[encourageless" + letters[i-1] + "]" + encourageless_dict[i].format(name)+'\n')

for i in rewardless_dict.keys():
    f.writelines("[rewardless" + letters[i-1] + "]" + rewardless_dict[i].format(name)+'\n')

for i in reward_dict.keys():
    f.writelines("[reward" + letters[i-1] + "]" + reward_dict[i].format(name)+'\n')

for j in guess_dict.keys():
    for i in range(51):
        f.writelines("[guess"+letters[j-1]+str(i)+"]"+guess_dict[j].format(i)+'\n')

for j in second_dict.keys():
    for i in range(51):
        f.writelines("[second"+letters[j-1]+str(i)+"]"+second_dict[j].format(name,i)+'\n')

f.close()
