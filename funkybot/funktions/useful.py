#==== Description ====
"""
Contains the useful FunkyBot commands
"""

from funktions import helpers as h, constant as c
import random
import re
from reminder import reminder
from poll import poll
from cardfetcher import cardfetcher as cf
from wikifetcher import wikifetcher as wf
from errors import errors

#==== Convert a number to binary ====
def toBin(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    
    #Parse number, convert it to usable string
    try:
        number = h.parse(message.content, "binary", 1, 1)
    except errors.Error as e:
        raise e
    
    for i in set(number): number = i #Change number back to int

    try:
        quotient = int(number)
        if quotient == 0:
            value = 0
        elif quotient > 65535 or quotient < 0:
            raise RuntimeError('Invalid number')
        else:
            while quotient != 0:
                remainder = quotient % 2
                quotient = int((quotient - remainder) / 2)
                value = str(remainder)+value
        return "%s in binary is: %s" % (number, value)
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("binary")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("binary")

#==== Convert a number to hexadecimal ====
def toHex(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    
    #Parse number, convert it to usable string
    try:
        number = h.parse(message.content, "hex", 1, 1)
    except errors.Error as e:
        raise e

    for i in set(number): number = i #Change number back to int

    try:
        quotient = int(number)
        if quotient == 0:
            value = 0
        elif quotient > 65535 or quotient < 0:
            raise RuntimeError('Invalid number')
        else:
            while quotient != 0:
                remainder = quotient % 16
                quotient = int((quotient - remainder) / 16)
                if remainder >= 10:
                    remainder = chr(remainder + 55)
                value = str(remainder)+value
        return "%s in hexadecimal is: %s" % (number, value)
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("hex")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("hex")

#==== Fetch a card ====
def fetchCard(message,apiHeaders):
    toReturn = []
    
    #Parse card name
    try:
        cards = h.parse(message.content, "magic", 1, 3)
    except errors.Error as e:
        raise e
    
    for i in cards:
        result = cf.fetchCard(i,apiHeaders)
        
        if isinstance(result, list):
            toReturn = toReturn + result
        else:
            toReturn.append(result)

    return toReturn

#==== Setup a poll ====
def makePoll(message):
    optDict = {}
    description = ""
    results = []

    try:
        options = h.parse(message.content, "poll", 2, 5)
    except errors.Error as e:
        raise e
    
    question = (re.sub("(\[\[.*\]\])|(!POLL)", "",
                       message.content, flags=re.IGNORECASE))
            
    return poll.Poll(message.author, question, options)

#==== Analyze poll results ====
def finishPoll(message,poll):
    results = {}
    toReturn = c.POLL_END % (poll.author, c.LINE_BREAK + poll.question)

    for r in message.reactions:
        if r.emoji in poll.options:
            results[r.emoji] = r.count - 1

    totalVotes = sum(results.values())

    for r in results:
        if totalVotes == 0:
            percent = 0
        else:
            percent = int((results[r]/totalVotes)*100)
            
        bar = chr(0x25A0) * int(percent / 5)
        spaces = ' ' * (20 - len(bar))

        toReturn = (toReturn + "\n"
                    + h.blockQuote(poll.options[r])
                    + h.blockQuote("`[%s%s]` %s votes, %s%%" %
                                   (bar, spaces, results[r], percent)))

    return toReturn

#==== Create a Reminder ====
def makeReminder(message,announcement=False):
    if announcement:
        cmd = "announce"
    else:
        cmd = "remind"
        
    try:
        timeArgs = h.parse(message.content, cmd, 1, 3)
    except errors.Error as e:
        raise e

    #Argument is a datetime
    if '/' in timeArgs[0]:
        duration = h.convertDateTime(timeArgs)
        date = True
    #Argument is a duration
    else: 
        duration = h.convertDurationTime(timeArgs)
        date = False

    if date and duration == None: #Datetime was not parsed correctly
        raise errors.CustomCommandException(cmd, "bad_date")
    elif date and duration <= 0: #Datetime is negative
        raise errors.CustomCommandException(cmd, "negative_date")
    elif not date and duration == None: #Duration was formatted incorrectly
        raise errors.CustomCommandException(cmd, "bad_duration")
    elif not date and duration > 2592000: #Duration over 30 days
        raise errors.CustomCommandException(cmd, "too_long")
    elif not date and duration <= 0: #Duration empty or negative
        raise errors.CustomCommandException(cmd, "no_duration")

    if announcement:
        timer = reminder.Announcement(duration=duration,msg=message,dt=date)
    else:
        timer = reminder.Reminder(duration=duration,msg=message,dt=date)

    return timer

#==== Send confirmation message of reminder ====
def confirmReminder(message,timer):
    if isinstance(timer, str): #Something went wrong, so an error was sent in
        return timer
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
    try:
        number = h.parse(message.content, "roll", 1, 1)
    except errors.Error as e:
        raise e
    
    for i in set(number): number = i #Convert back to a number
    
    try:
        number = int(number)
        if number <= 0 or number > 1000:
            raise RuntimeError('Invalid number')
        else:
            return "You rolled %s!" % random.randint(1,number)
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("roll")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("roll")

#==== Fetch a Wikipedia article ====
def fetchWiki(message,apiHeaders):
    try:
        terms = h.parse(message.content, "wiki", 1, 1)
    except errors.Error as e:
        raise e

    for i in set(terms): terms = i #Convert back to a string

    return wf.fetchArticle(terms,apiHeaders)
