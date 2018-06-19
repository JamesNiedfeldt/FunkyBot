#==== Description ====
"""
The main functionality of FunkyBot is here
"""

import random
import re
import urllib.request, urllib.error
import os
import time
import funkyHelp

#==== Answer a yes/no question ====
def eightBall():
    file = open(filePath('Lists/answers.txt'), 'r')
    answers = file.readlines()
    randInt = random.randint(0, (len(answers)) - 1)
    file.close()

    return answers[randInt]

#==== Convert a number to binary ====
def toBin(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    #Parse number, convert it to usable string
    number = parse(message.content)
    
    if len(number) == 0: #Nothing to convert
        return "I couldn't understand your command!"
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

#==== Choose randomly from choices ====
def choose(message):
    #Parse choices
    choices = parse(message.content)

    if len(choices) == 0: #No choices
        return "I couldn't understand your command!"
    elif len(choices) == 1: #Not enough choices
        return "I need more than one thing to choose from!"
    elif len(choices) > 10: #Too many choices
        return "There are too many things to choose from!"

    #for i in set(choices): choices[i] = i #Turn back to strings

    return "I choose %s!" % choices[random.randint(0,len(choices)-1)]
    
#==== Introduce FunkyBot ====
def sayHello(sender,version,uptime):
    return("""
    Hello %s, my name is FunkyBot! I am a simple bot made for fun as my creator's personal project. Here's some information about me:

    **Current version:** %s 
    **Current uptime:** %s 
    """ % (sender.display_name, version, formatTime(uptime)))

#==== Send a help message ====
def sendHelp(message):
    #Parse command
    command = parse(message.content)

    if len(command) == 0: #Nothing to help with
        return """
I couldn't understand the command! Make sure you send a single command you want help with in double brackets and don't include options. For example: `!help [[!binary]]`

If you want a list of commands, send `!commands`.
    """
    elif len(command) > 1: #Too many commands
        return "I can only help you with one command at a time!"
    else:
        for i in set(command): command = i #Change back to string
        return funkyHelp.getHelp(command)
    
#==== Get a list of commands ====
def commandList():
    return("""
    Here are my commands:\n
    - **Information:** `!commands` `!hello` `!help [[X]]`
    - **Useful:** `!binary [[X]]` `!hex [[X]]` `!magic [[X|...|...]]` `!roll [[X]]`
    - **Fun:** `!ask` `!choose [[X|Y|...]]` `!joke` `!react` `!rate [[X]]` `!shibe`
\nIf you need specific information on commands or general use, send the `!help` command with the command you want help with. For example, `!help [[!ask]]`.
    """)
    
    
#==== Convert a number to hexadecimal ====
def toHex(message):
    remainder = -1 #Remainder used for conversion
    value = "" #Value to print
    #Parse number, convert it to usable string
    number = parse(message.content)

    if len(number) == 0: #Nothing to convert
        return "I couldn't understand your command!"
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

#==== Tell a joke ====
def findOneLiner():
    file = open(filePath('Lists/jokes.txt'), 'r')
    jokes = file.readlines()
    randInt = random.randint(0, (len(jokes)) - 1)
    file.close()

    return jokes[randInt]

#==== Fetch a card ====
def fetchCard(message):
    cardID = "" #Gatherer ID
    search = "" #Search query
    toReturn = [] #List of found cards to return
    
    #Parse card name
    cards = parse(message.content)
    if len(cards) > 3: #Too many cards in search
        toReturn.append("That's too many cards to search for!")
        return list(toReturn)
    elif len(cards) == 0: #Nothing to search for
        toReturn.append("I couldn't understand your command!")
        return list(toReturn)
    for i in set(cards):
        i = i.split('/')[0]
        j = urllib.request.quote(i.encode('utf-8'))
        #Search for card id
        search = urllib.request.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%s" % j.replace("&", "%26")).read()
        try:
            cardID = re.search(b"multiverseid=([0-9]*)", search).group(1)
            #Parse card ID, convert it to usable string
            cardID = re.findall("b'([^\[\]]*)'", str(cardID))
            for d in set(cardID): cardID = d
            toReturn.append("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card&.jpg" % cardID)
        except AttributeError: #Couldn't find card
            toReturn.append("Sorry, I couldn't find \"%s\" !" % i)
    return list(toReturn)

#==== Send random reaction image ====
def reactionPic():
    pics = os.listdir(filePath("reaction_pics/")) #Paths to images
    selection = "" #Image path to post
    found = False #Image found or not

    try:
        validFolder(pics) #Check if folder is empty
        while not found: #Search for a valid file path
            selection = random.choice(pics)
            if (selection != "Thumbs.db" and
                selection != ".gitkeep"):
                found = True
                return filePath("reaction_pics/%s" % selection)
    except RuntimeError: #Folder is empty
        raise

#==== Rate something ====
def rateSomething(message):
    with open(filePath('Lists/ratings.txt'),'r') as file:
        ratings = file.readlines()
        file.close()
    score = random.randint(1, 10)
    
    #Parse string
    toRate = parse(message.content)

    if len(toRate) == 0: #Nothing to rate
        return "I couldn't understand your command!"
    elif len(toRate) > 1: #Too many things to rate
        return "I can only rate one thing!"

    for i in set(toRate): toRate = i #Change back to string

    if toRate.upper() in {
        "FUNKYBOT","FUNKY","YOU"}:
        return "I give myself an 11/10. Literally the best ever." 
    elif toRate.upper() in {
        "ME","MYSELF"}:
        return "I give %s a %s out of 10. %s" % (message.author.display_name, score, ratings[score-1])
    else:
        return "I give %s a %s out of 10. %s" % (toRate, score, ratings[score-1])

#==== Roll a die ====
def rollDice(message):
    #Parse number, convert it to usable string
    number = parse(message.content)

    if len(number) == 0: #No number to roll
        return "I couldn't understand your command!"
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

#==== Send random Shiba Inu picture ====
def shibaPic():
    pics = os.listdir(filePath("shiba_pics/")) #Paths to images
    selection = "" #Image path to post
    found = False #Image found or not

    try:
        validFolder(pics) #Check if folder is empty
        while not found: #Search for a valid file path
            selection = random.choice(pics)
            if (selection != "Thumbs.db" and
                selection != ".gitkeep"):
                found = True
                return filePath("shiba_pics/%s" % selection)
    except RuntimeError: #Folder is empty
        raise

#==== NON-COMMAND METHODS ====

#==== Parse a string ====
def parse(string):
    contents = re.findall("\[\[([^\[\]]*)\]\]", string) #Find contents of '[[]]'
    
    if len(contents) == 0: #Nothing was found
        contents.clear()
        return contents
    
    contents = re.split("\|", contents[0])  #Split multiple deliminated with '|'
    
    for i in set(contents):
        if i == "": #Is there a blank entry?
           contents.clear()
           pass
    return contents
    
#==== Log deleted messages ====
def logMessage(message):
    try:
        log = open(filePath('Logs/'+str(message.server)+'-log.txt'),'a+')
        toLog = "%s - %s - %s: %s\n" % (message.timestamp.strftime("%Y-%b-%d %H:%M"),message.channel,message.author.name,message.content)
        log.write(toLog)
        log.close()
    except UnicodeError: #Message or username contains non-unicode char
        raise

#==== Check directories for valid images ====
def validFolder(files):
    if len(files) > 1:
        return
    else:
        raise RuntimeError

#==== Calculate uptime ====
def upTime():
    return time.time()

#==== Format uptime ====
def formatTime(inTime):
    totalSec = int(time.time() - inTime)

    seconds = totalSec % 60
    minutes = int((totalSec % 3600) / 60)
    hours = int((totalSec % 86400) / 3600)
    days = int(totalSec / 86400)

    formatted = "%s days, %s hours, %s minutes, and %s seconds" % (days, hours, minutes, seconds)

    return formatted

#==== Return relative path ====
def filePath(directory):
    absolute = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(absolute, directory)
    return path
