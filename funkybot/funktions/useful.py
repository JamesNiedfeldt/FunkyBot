#==== Description ====
"""
Contains the useful FunkyBot commands
"""

#==== Imports ====
import random
import re

from helpers import (helper_functions as h, constant as c, global_vars as g,
                     card_fetcher as cf, wiki_fetcher as wf, calculator as ca,
                     game_fetcher as gf)
from helpers.objects import reminder, poll
from errors import errors

#==== Convert a number to binary ====
def toBin(message):
    toReturn = ""
    
    #Parse number, convert it to usable string
    try:
        numbers = h.parseArgs(message.content, "binary", 1, g.props['binary_max_args'])
    except errors.Error as e:
        raise e

    try:
        for q in numbers:
            quotient = int(q)
            remainder = -1
            value = ""
            
            if quotient == 0:
                value = 0
            elif quotient > 65535 or quotient < 0:
                raise RuntimeError('Invalid number')
            else:
                while quotient != 0:
                    remainder = quotient % 2
                    quotient = int((quotient - remainder) / 2)
                    value = str(remainder)+value
                    
            toReturn = toReturn + "%s in binary is: %s\n" % (q, value)
            
        return toReturn.rstrip() #Get rid of newline
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("binary")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("binary")

#==== Calculate an equation ====
def calc(message):
    toReturn = ""
    
    #Parse arguments
    try:
        eq = h.parseArgs(message.content, "calc", 1, 1)
        for r in eq: eq = r #Convert to string
    except errors.Error as e:
        raise e

    try:
        answer = ca.calculate(eq)
        toReturn = "Here's what I calculated:" + c.LINE_BREAK
        toReturn = toReturn + "`" + " ".join(eq.split()) + "`\n= %s" % answer

        return toReturn
    except errors.Error as e:
        raise e
    except ZeroDivisionError:
        return "It's not possible to divide by zero. Are you trying to end the world?! %s" % c.RETRY_EQUATION
    except Exception as e:
        if str(e) == "math domain error": #Probably sqrt of negative
            return "It's not possible to take the square root of a negative number. %s" % c.RETRY_EQUATION
        elif isinstance(e, OverflowError):
            return "Sorry, the answer was too big for me to calculate."
        else:
            if not isinstance(e, IndexError) or not isinstance(e, ValueError):
                h.logException(e)
            return "Sorry, I couldn't finish the calculation. %s" % c.RETRY_EQUATION

#==== Convert a number to hexadecimal ====
def toHex(message):
    toReturn = ""
    
    #Parse number, convert it to usable string
    try:
        numbers = h.parseArgs(message.content, "hex", 1, g.props['hex_max_args'])
    except errors.Error as e:
        raise e

    try:
        for q in numbers:
            quotient = int(q)
            remainder = -1
            value = ""
            
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
                    
            toReturn = toReturn + "%s in hexadecimal is: %s\n" % (q, value)
            
        return toReturn.rstrip() #Get rid of newline
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("hex")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("hex")

#==== Fetch a game from GiantBomb ====
def fetchGame(message):
    try:
        terms = h.parseArgs(message.content, "game", 1, 1)
    except errors.Error as e:
        raise e

    for i in set(terms): terms = i #Convert back to a string

    return gf.fetchGame(terms)

#==== Fetch a card ====
def fetchCard(message):
    toReturn = []
    
    #Parse card name
    try:
        cards = h.parseArgs(message.content, "magic", 1, 3)
    except errors.Error as e:
        raise e
    
    for i in cards:
        if i.startswith("|"):
            raise errors.TooFewArgumentsException("magic")
        else:
            result = cf.fetchCard(i)
        
            if isinstance(result, list):
                toReturn = toReturn + result
            else:
                toReturn.append(result)

    return toReturn

#==== Setup a poll ====
def makePoll(message):
    try:
        options = h.parseArgs(message.content, "poll", 2, 5)
    except errors.Error as e:
        raise e
    
    question = (re.sub("\[([^\[\]]*)\]", "",
                       message.content.split(' ',1)[1], flags=re.IGNORECASE))
            
    return poll.Poll(message, question, options)

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
            
        bar = "\N{BLACK SQUARE}" * int(percent / 5)
        spaces = ' ' * (20 - len(bar))

        toReturn = (toReturn + "\n"
                    + h.blockQuote(poll.options[r])
                    + h.blockQuote("`[%s%s]` %s votes, %s%%" %
                                   (bar, spaces, results[r], percent)))
        
    toReturn = (toReturn + c.LINE_BREAK
                + "Poll link: " + message.jump_url)

    return toReturn

#==== Create a Reminder object with duration ====
def makeDurationReminder(message):
    try:
        timeArgs = h.parseArgs(message.content, "time", 1, 3)
    except errors.Error as e:
        raise e

    duration = h.convertDurationTime(timeArgs)


    if duration == None: #Duration was formatted incorrectly
        raise errors.CustomCommandException("time", "bad_duration")
    elif duration > g.props['time_max_duration'] * 86400: #Duration longer than set property
        raise errors.CustomCommandException("time", "too_long")
    elif duration < 1: #Duration less than 1 second
        raise errors.CustomCommandException("time", "no_duration")

    timer = reminder.Reminder(duration=duration,msg=message,dt=False)

    return timer

#==== Create a Reminder object with date ====
def makeDateReminder(message, announcement=False):
    if announcement:
        cmd = "announce"
    else:
        cmd = "remind"
        
    try:
        timeArgs = h.parseArgs(message.content, cmd, 1, 1)
    except errors.Error as e:
        raise e

    duration = h.convertDateTime(timeArgs)
    date = True

    if duration == None: #Datetime was not parsed correctly
        raise errors.CustomCommandException(cmd, "bad_date")
    elif duration <= 0: #Datetime is negative
        raise errors.CustomCommandException(cmd, "negative_date")

    if announcement:
        timer = reminder.Announcement(duration=duration,msg=message,dt=True)
    else:
        timer = reminder.Reminder(duration=duration,msg=message,dt=True)

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

        if isinstance(timer, reminder.Announcement):
            confirmation = c.ANNOUNCE_CONFIRM_1 % (h.escapeCodeBlock(message.author.display_name),
                                                   formattedTime)
            reminderText = h.escapeCodeBlock(
                re.split("@everyone ", timer.message, maxsplit=1)[1])
            
        else:
            confirmation = c.REMIND_CONFIRM_1 % (h.escapeCodeBlock(message.author.display_name),
                                                 formattedTime)
            reminderText = h.escapeCodeBlock(
                re.split("\<*\> ", timer.message, maxsplit=1)[1])

        if reminderText == "":
            reminderText = "*No message was given*"

        return (confirmation
                + h.blockQuote(reminderText)
                + "\n" + c.REMIND_CONFIRM_2)

#==== Send confirmation message of reminder ====
def startReminder(timer):
    timer.beginThread()
    g.db.insertReminder(timer)

    try:
        if timer.live:
            return "Ok, I set a reminder for you!"
        else:
            raise RuntimeError("Reminder timer wasn't live")
    except Exception as e:
        h.logException(e)
        return "Sorry, I couldn't make the reminder!"

#==== Roll a die ====
def rollDice(message):
    ords = ['first','second','third','fourth','fifth',
            'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    toReturn = ""
    index = 0
    total = 0
    
    try:
        numbers = h.parseArgs(message.content, "roll", 1, g.props['roll_max_args'])
    except errors.Error as e:
        raise e
    
    try:
        for n in numbers:
            number = int(n)
            
            if number <= 1 or number > 1000:
                raise RuntimeError('Invalid number')
            else:
                if len(numbers) == 1:
                    return "You rolled %s!" % random.randint(1,number)
                else:
                    roll = random.randint(1,number)
                    total = total + roll
                    toReturn = toReturn + "Your %s roll was: %s\n" % (ords[index], roll)
                    index = index + 1

        toReturn = toReturn + "\nYour total roll was %s!" % total
        return toReturn
        
    except ValueError: #Non-integer sent
        raise errors.BadValueException("roll")
    except RuntimeError: #Non-integer sent or invalid number
        raise errors.BadNumberException("roll")

#==== Fetch a Wikipedia article ====
def fetchWiki(message):
    try:
        terms = h.parseArgs(message.content, "wiki", 1, 1)
    except errors.Error as e:
        raise e

    for i in set(terms): terms = i #Convert back to a string

    return wf.fetchArticle(terms)
