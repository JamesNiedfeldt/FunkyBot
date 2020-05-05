#==== Description ====
"""
Contains the useful FunkyBot commands
"""

from funktions import helpers as h
import random
import re
from reminder import reminder
from cardfetcher import cardfetcher as cf

#==== Convert a number to binary ====
def toBin(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    #Parse number, convert it to usable string
    number = h.parse(message.content)
    
    if len(number) == 0: #Nothing to convert
        return h.badArgs("binary")
    elif len(number) > 1: #Too many numbers
        return "I can only convert one number!"
    
    for i in set(number): number = i #Change number back to int

    try:
        quotient = int(number)
        if quotient == 0:
            value = 0
        elif quotient > 1023 or quotient < 0:
            raise ValueError('Invalid number')
        else:
            while quotient != 0:
                remainder = quotient % 2
                quotient = int((quotient - remainder) / 2)
                value = str(remainder)+value
        return "%s in binary is: %s" % (number, value)
        
    except TypeError: #Non-integer sent
        return "Sorry, I can't convert %s to binary!" % number
    except ValueError: #Non-integer sent or invalid number
        return "Sorry, I can't convert %s to binary!" % number

#==== Convert a number to hexadecimal ====
def toHex(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    #Parse number, convert it to usable string
    number = h.parse(message.content)

    if len(number) == 0: #Nothing to convert
        return h.badArgs("hex")
    elif len(number) > 1: #Too many numbers
        return "I can only convert one number!"

    for i in set(number): number = i #Change number back to int

    try:
        quotient = int(number)
        if quotient == 0:
            value = 0
        elif quotient > 65535 or quotient < 0:
            raise ValueError('Invalid number')
        else:
            while quotient != 0:
                remainder = quotient % 16
                quotient = int((quotient - remainder) / 16)
                if remainder >= 10:
                    remainder = chr(remainder + 55)
                value = str(remainder)+value
        return "%s in hexadecimal is: %s" % (number, value)
        
    except TypeError: #Non-integer sent
        return "Sorry, I can't convert %s to hexadecimal!" % number
    except ValueError: #Non-integer sent or invalid number
        return "Sorry, I can't convert %s to hexadecimal!" % number

#==== Fetch a card ====
def fetchCard(message):
    toReturn = []
    
    #Parse card name
    cards = h.parse(message.content)
    if len(cards) > 3: #Too many cards in search
        toReturn.append([None, "That's too many cards to search for!"])
        return list(toReturn)
    elif len(cards) == 0: #Nothing to search for
        toReturn.append([None, h.badArgs("magic")])
        return list(toReturn)
    for i in cards:
        result = cf.fetchCard(i)
        
        if not all(isinstance(r, list) for r in result):
            toReturn.append(result)
        else:
            for l in result:
                if type(l) == list:
                    toReturn.append(l)

    return toReturn

#==== Create a Reminder ====
def makeReminder(message,announcement=False):
    timeArgs = h.parse(message.content)

    if len(timeArgs) == 0:
        return None

    if len(timeArgs) < 1:
        duration = 30
    else:
        #Argument is a datetime
        if '/' in timeArgs[0]:
            duration = h.convertDateTime(timeArgs)
            date = True
        #Argument is a duration
        else: 
            duration = h.convertDurationTime(timeArgs)
            date = False

    if duration == None:
        return None

    if announcement:
        timer = reminder.Announcement(duration=duration,msg=message,dt=date)
    else:
        timer = reminder.Reminder(duration=duration,msg=message,dt=date)

    return timer

#==== Send confirmation message of reminder ====
def confirmReminder(message,timer):
    if timer == None:
        return h.badArgs('remind')
    else:
        if timer.dt:
            formattedTime = h.formatTime(timer.duration - h.getTime())
        else:
            formattedTime = h.formatTime(timer.duration)
        return "Ok %s, I will remind you in %s. If that is ok, reply with `!yes`. If not, reply with `!no`." % (
            message.author.display_name, formattedTime)

#==== Send confirmation message of reminder ====
def startReminder(timer):
    timer.beginThread()
    reminder.database.insertToDb(timer)

    if timer.live:
        return "Ok, I set a reminder for you!"
    else:
        return "Sorry, something went wrong!"

#==== Roll a die ====
def rollDice(message):
    #Parse number, convert it to usable string
    number = h.parse(message.content)

    if len(number) == 0: #No number to roll
        return h.badArgs("roll")
    elif len(number) > 1: #Too many dies to roll
        return "I can only roll one die!"
    
    for i in set(number): number = i #Convert back to a number
    
    try:
        number = int(number)
        if number <= 0 or number > 1000:
            raise ValueError('Invalid number')
        else:
            return "You rolled %s!" % random.randint(1,number)
        
    except TypeError: #Non-integer sent
        return "I can't roll a die with %s sides!" % number
    except ValueError: #Non-integer sent or invalid number
        return "I can't roll a die with %s sides!" % number
