#code for the bisection number game, start with logical steps
#step 1: initialize variables, import modules
import random
import bisect

#step 2: generate strings for first interactions,
#pull a random phrase from correct set
intro_set = ['Nice to meet you, I\'m QT! Let\'s play a game! Think of a number between 1 and 100',
             'Guess a number between 1 and 100!'] 
    #make this a dictionary/set, giving each entry a line break makes it easier to read
    #i can nest dictionaries
random_phrase_ix = random.randrange(0,len(intro_set))
intro_string = intro_set[random_phrase_ix]
    #use get method for the intro set dict.get(key, set return value)
start = input('Let\'s start! ') #type ok
print(intro_string)

#step 3: ask if guess is correct, use bisection alg
    #identify variables to compare in boolean operations ex: guess, high bound, low bound, random_w_guess
    #print statements after every line to follow logic flow when debugging
print('Is this your guess?')
high = 101
low = -1
half_guess = int((high-low)/2)
random_guess = 
print(half_guess)

guess = bisect.bisect(guess_list, half_guess)+half_guess
print(guess+low)

#step 4: read response from participant
#for now use button press

#step 5: repeat - make the game ongoing
    #use 0/1 or true/false instead of string
while start == 'ok':
    val = input('Is my guess correct? ')
    if val == 'no':
        val2 = input('higher or lower? ')
        if val2 == 'higher':
            guess_list = [guess,100]
        if val2 == 'lower':
            guess_list = [0,guess]
        half_guess = int((high-low)/2)
        guess = bisect.bisect(guess_list, half_guess)+half_guess
        print(guess+guess_list[0])
    if val == 'yes':
        print('I win!')
        quit()
        



