#code for the bisection number game, start with logical steps
#step 1: initialize variables, import modules
import random

nocounter = 0
yescounter = 0
high = 101
low = -1

#use 0/1 or true/false instead of string
start = 'ok'
while start == 'ok':
    half_range = int((high-low)/2)
    current = half_range+low
    random_add = random.randrange(-half_range,half_range) #never add on outside of the guessing range
    QT = current+random_add
    print("QT Guess is: "+str(QT))
    print("Current is {} and random addition is {}.".format(current,random_add))
    print("High is {} and low is {}.".format(high,low))

    val = input('Is my guess correct? (0 no, 1 yes) ')
    if val is "0":
        val2 = input('higher(1) or lower(0)? ')
        nocounter += 1
        if val2 is "1":
            low = QT
            yescounter += 1
        if val2 is "0":
            high = QT
            nocounter += 1
    else:
        yescounter += 1
        print("Number of yes: "+str(yescounter)+". Number of no: "+str(nocounter))
        print('I win!')
        quit()
        



