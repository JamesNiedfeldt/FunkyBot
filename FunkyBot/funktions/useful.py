#==== Description ====
"""
Contains the useful FunkyBot commands
"""

from funktions import helpers as h
import random
import requests
import re
from reminder import reminder

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
        if quotient <= 0 or quotient > 1024:
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
        if quotient <= 0 or quotient > 65535:
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
    URL = "https://api.scryfall.com/cards/search"
    toReturn = []
    
    #Parse card name
    cards = h.parse(message.content)
    if len(cards) > 3: #Too many cards in search
        toReturn.append("That's too many cards to search for!")
        return list(toReturn)
    elif len(cards) == 0: #Nothing to search for
        toReturn.append(h.badArgs("magic"))
        return list(toReturn)
    for i in set(cards):
        i = i.split('/')[0]
        c = i.encode('utf-8')
        
        response = requests.get(url = URL, params = {'q':c})
        results = response.json()

        try:
            if(results['object'] == "list"): #Found a list
                card = results['data'][0]

                if(card['layout'] == "transform"): #Double-faced card
                    transform = ""
                    for f in card['card_faces']:
                        transform = transform + "\n" + f['image_uris']['normal']
                    toReturn.append(transform)
                else: #Normal card
                    toReturn.append(card['image_uris']['normal'])
                    
            else: #No results or got something weird
                toReturn.append("Sorry, I couldn't find \"%s\"!" % i)

        except KeyError as e: #Couldn't find JSON key
            toReturn = "Something went wrong!"
            
    return list(toReturn)

#==== Create a Reminder ====
def makeReminder(message,announcement=False):
    duration = 0
    timeArgs = h.parse(message.content)

    if(len(timeArgs) == 0):
        return None

    if(len(timeArgs) < 1):
        duration = 30
    else:
        if(len(timeArgs) > 3):
            timeArgs = timeArgs[0:3]
        for i in set(timeArgs):
            timeArgs = i
            if('s' in i):
                i = "".join(re.split("\D",i))
                duration = duration + float(i)
            elif('m' in i):
                i = "".join(re.split("\D",i))
                duration = duration + float(i)*60
            elif('h' in i):
                i = "".join(re.split("\D",i))
                duration = duration + float(i)*3600
            elif('d' in i):
                i = "".join(re.split("\D",i))
                duration = duration + float(i)*86400

    #Max of 30 days
    if(duration > 2592000):
        duration = 2592000
    elif(duration == 0):
        duration = 300

    if(announcement):
        timer = reminder.Announcement(duration=duration,msg=message)
    else:
        timer = reminder.Reminder(duration=duration,msg=message)

    return timer

#==== Send confirmation message of reminder ====
def confirmReminder(message,timer):
    if(timer == None):
        return h.badArgs('remind')
    else:
        return "Ok %s, I will remind you in %s. If that is ok, reply with `!yes`. If not, reply with `!no`." % (
            message.author.display_name,h.formatTime(timer.duration))

#==== Send confirmation message of reminder ====
def startReminder(timer):
    timer.beginThread()
    reminder.database.insertToDb(timer)

    if(timer.live):
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
