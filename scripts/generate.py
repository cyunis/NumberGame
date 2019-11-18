#!/usr/bin/env python
# -*- coding: utf-8 -*-
name = 'NAME'
hand = 'right'
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']

clarify_dict = {1: 'Sorry I didn’t see that, could you repeat that answer for me please?',
    2: "I think that was a yes. Could you make a thumbs up again for me please?",
    3: "I think that was a no. Could you make a thumbs down again for me please?",
    4: "Could you please show me that answer again {}?",
    5: "Sorry I didn’t see that {}, could you repeat that answer for me please?",
    6: "Hey could you please show me that answer again?",
    7: 'I didn’t understand I need you to show me again please!',
    8: 'I didn’t see that can you please show me again!',
    9: 'Was that a thumbs up or down? Can you show me again please?',
    10: '{} please show me what you did again I missed it.',
    11: 'Can you show me what you did again please?'} 
#2/3 and 9/10 should be used depending on what the gesture was supposed to be

encourage_dict = {1: 'Good job {}!',
    2: 'That was your best one so far! Keep up the good work!',
    3: 'I can tell you are trying really hard {}, nice job!',
    4: 'You are getting better at this {}, wow!',
    5: 'I know this is hard {}, keep trying!',
    6: 'Hooray! Let’s play again {}!',
    7: 'Hey, good job!',
    8: 'That was your best one so far {}! Keep up the good work!',
    9: 'I can tell you are trying really hard, nice job!',
    10: 'Everyone, {} is getting better at this!',
    11: 'Keep trying, I know this is hard but you got it!',
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
    4: 'Hooray keep it up!',
    5: '{} you made me smile.',
    6: 'I think that {} made one of the best gestures I’ve ever seen!',
    7: 'That was a good gesture!',
    8: '{} is very good at this game.',
    9: 'Keep showing me what you got!',
    10: 'This game is fun to play with you!',
    11: 'You are playing well!',
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
    8: 'I guess {}, am I wrong?'}
#make sure name and number are in the right spot for every phrase - use 0 or 1 in the brackets to call in order
#higher or lower
second_dict = {1: 'Hey {} is your number bigger than {}? Show me yes or no.',
    2: 'Oh no, I guessed {1}. Did I guess smaller than your number?',
    3: 'Hmm is {1} smaller than your number?',
    4: 'Hey is your number bigger than {1}? Show me yes or no.',
    5: 'Aw man {}, I guessed {}. Did I guess smaller than your number?',
    6: 'Hmm {}, is {} smaller than your number?',
    7: 'Hey is your number bigger than {1}? Show me yes or no please.',
    8: 'Oh no, I guessed {1}! Did I guess smaller than your number?',
    9: 'Hmm tell me {} is {} smaller than your number?'} 

filler_dict = {1: 'I see that.',
    2: 'I am here to play this game with you, thanks for playing with me.',
    3: 'I can tell you like playing games.',
    4: '{} is a cool name I like it.',
    5: 'I think that this game is hard.',
    6: 'Hooray! I am so excited to guess what you’re thinking.',
    7: 'Hey {}, thanks for playing!',
    8: 'This is my favorite game to play with you!',
    9: 'Hey {} I like being part of a science experiment, this is fun.',
    10: 'Everyone, I am playing a game with {}!',
    11: 'Keep showing me what you’re doing so I can play with you.',
    12: 'Hooray I like this!',
    13: 'Lets keep playing this game!',
    14: 'Cool I saw that.',
    15: 'I’m thinking really hard!',
    16: 'I think I’m going to win this game.',
    17: 'I am going to guess another number until I get it.',
    18: 'Yay this is fun to play.',
    19: 'I am smiling a lot.',
    20: 'I play a lot of games like this.'}


f = open("script.txt",mode = 'w',encoding = 'utf-8')

f.writelines('[wiggins]'+'<prosody rate="slow">In front of you is a list of words. *question1* Please tell me if these words describe you, using a number 1, 2, 3, 4 or 5. If the word does not describe you at all pick 1, if the word describes you a lot pick 5. If its something in between pick 2, 3 or 4.</prosody>\n')
f.writelines('[wigginsorthosis]'+'<prosody rate="slow">In front of you is a list of words. *question1* Please tell me if these words describe the robot on your arm, using a number 1, 2, 3, 4 or 5. If the word does not describe you at all pick 1, if the word describes you a lot pick 5. If its something in between pick 2, 3 or 4.</prosody>\n')
f.writelines('[bad]'+'<prosody rate="slow">The *loud* first word is bad.</prosody>\n')
f.writelines('[good]'+'<prosody rate="slow">The *loud* second word is good.</prosody>\n')
f.writelines('[notfriendly]'+'<prosody rate="slow">The *loud* third word is not friendly.</prosody>\n')
f.writelines('[friendly]'+'<prosody rate="slow">The *loud* fourth word is friendly.</prosody>\n')
f.writelines('[cold]'+'<prosody rate="slow">The *loud* fifth word is cold.</prosody>\n')
f.writelines('[warm]'+'<prosody rate="slow">The *loud* sixth word is warm.</prosody>\n')
f.writelines('[unpleasant]'+'<prosody rate="slow">The *loud* seventh word is unpleasant.</prosody>\n')
f.writelines('[pleasant]'+'<prosody rate="slow">The *loud* eighth word is pleasant.</prosody>\n')
f.writelines('[cruel]'+'<prosody rate="slow">The *loud* ninth word is cruel.</prosody>\n')
f.writelines('[kind]'+'<prosody rate="slow">The *loud* tenth word is kind.</prosody>\n')
f.writelines('[harsh]'+'<prosody rate="slow">The *loud* eleventh word is harsh.</prosody>\n')
f.writelines('[sweet]'+'<prosody rate="slow">The *loud* twelfth word is sweet.</prosody>\n')
f.writelines('[useful]'+'<prosody rate="slow">The *loud* thirteenth word is useful.</prosody>\n')
f.writelines('[valuable]'+'<prosody rate="slow">The *loud* fourteenth word is valuable.</prosody>\n')
f.writelines('[helpful]'+'<prosody rate="slow">The *loud* fifteenth word is helpful.</prosody>\n')
f.writelines('[skillful]'+'<prosody rate="slow">The *loud* sixteenth word is skillful.</prosody>\n')
f.writelines('[clever]'+'<prosody rate="slow">The *loud* seventeenth word is clever.</prosody>\n')
f.writelines('[intelligent]'+'<prosody rate="slow">The *loud* eighteenth word is intelligent.</prosody>\n')
f.writelines('[smart]'+'<prosody rate="slow">The *loud* nineteenth word is smart.</prosody>\n')
f.writelines('[intro1qt]'+'<prosody rate="slow">Hello, my name is QT Robot. What is your name?</prosody>\n')
f.writelines('[intro1comp]'+'<prosody rate="slow">Hello, my name is TQ Computer. What is your name?</prosody>\n')
f.writelines('[intro2]'+'<prosody rate="slow">Hi {} I would like to play a guessing game with you. In the game, I ask you questions, and you answer yes or no by using a thumbs up or a thumbs down with your {} hand.</prosody>\n'.format(name,hand)) 
f.writelines('[intro3]'+'<prosody rate="slow">Let’s practice.  Can you show me a thumbs up to say yes?</prosody>\n')
f.writelines('[intro4]'+'<prosody rate="slow">Awesome! Now can you show me a thumbs down to say no?</prosody>\n')
f.writelines('[intro5]'+'<prosody rate="slow">Thanks! During the game, please keep your hand flat and your arm on the arm rest until I ask you a question. If your thumb is going the wrong way, tell Catherine to push the green button. And just do your best.</prosody>\n')
f.writelines('[startgame]'+'<prosody rate="slow">Let\'s play now! Please think of a number between 1 and 50.</prosody>\n')
f.writelines('[another1]'+'<prosody rate="slow">Hooray I got it! Thanks {} for playing with me. Do you want to play again?</prosody>\n'.format(name))
f.writelines('[another2]'+'<prosody rate="slow">Hooray I guessed right! Do you want to play again please?</prosody>\n')
f.writelines('[another3]'+'<prosody rate="slow">Woo hoo that was fun! Do you want to play one more game?</prosody>\n')
f.writelines('[anotherchoice]'+'<prosody rate="slow">So fun! Do you want to play another game with the robot, play a game with the computer or stop playing?</prosody>\n')
f.writelines('[endgame]'+'<prosody rate="slow">Thanks for playing with me {}! Bye-bye!</prosody>\n'.format(name))

for i in clarify_dict.keys():
    f.writelines("[clarify" + letters[i-1] + "]" + "<prosody rate='slow'>" + clarify_dict[i].format(name) + "</prosody>" +'\n')

for i in encourage_dict.keys():
    f.writelines("[encourage" + letters[i-1] + "]" + "<prosody rate='slow'>" + encourage_dict[i].format(name) + "</prosody>" +'\n')

for i in encourageless_dict.keys():
    f.writelines("[encourageless" + letters[i-1] + "]" + "<prosody rate='slow'>" + encourageless_dict[i].format(name) + "</prosody>" +'\n')

for i in rewardless_dict.keys():
    f.writelines("[rewardless" + letters[i-1] + "]" + "<prosody rate='slow'>" + rewardless_dict[i].format(name) + "</prosody>" +'\n')

for i in reward_dict.keys():
    f.writelines("[reward" + letters[i-1] + "]" + "<prosody rate='slow'>" + reward_dict[i].format(name) + "</prosody>" +'\n')

for i in filler_dict.keys():
    f.writelines("[filler" + letters[i-1] + "]" + "<prosody rate='slow'>" + filler_dict[i].format(name) + "</prosody>" +'\n')

for j in guess_dict.keys():
    for i in range(51):
        f.writelines("[guess"+letters[j-1]+str(i)+"]"+ "<prosody rate='slow'>" + guess_dict[j].format(i) + "</prosody>" +'\n')

for j in second_dict.keys():
    for i in range(51):
        f.writelines("[second"+letters[j-1]+str(i)+"]"+ "<prosody rate='slow'>" + second_dict[j].format(name,i) + "</prosody>" + '\n')

f.close()
