#==== Description ====
"""
Contains the fun FunkyBot commands
"""

from funktions import helpers as h
import random
import os

#==== Answer a yes/no question ====
def eightBall():
    answers = h.getXmlTree("lists").findall("./list/[@type='answers']/answer")

    return random.choice(answers).text

#==== Choose randomly from choices ====
def choose(message):
    #Parse choices
    choices = h.parse(message.content)

    if len(choices) == 0: #No choices
        return h.badArgs("choose")
    elif len(choices) == 1: #Not enough choices
        return "I need more than one thing to choose from!"
    elif len(choices) > 10: #Too many choices
        return "There are too many things to choose from!"

    return "I choose %s!" % random.choice(choices)

#==== Tell a joke ====
def findOneLiner():
    answers = h.getXmlTree("lists").findall("./list/[@type='jokes']/joke")

    return random.choice(answers).text

#==== Send random reaction or shiba inu image ====
def randomPic(path):
    try:
        pics = os.listdir(h.filePath(path + '/')) #Paths to images
        selection = "" #Image path to post
        found = False #Image found or not

        h.validFolder(pics) #Check if folder is empty
        while not found: #Search for a valid file path
            selection = random.choice(pics)
            if (selection != "Thumbs.db" and
                selection != ".gitkeep"):
                found = True
                return h.filePath(path + '/' + selection)
    except FileNotFoundError: #Bad path
        raise
    except RuntimeError: #Folder is empty
        raise

#==== Rate something ====
def rateSomething(message):
    ratings = h.getXmlTree("lists").findall("./list/[@type='ratings']/rating")
    rank = random.choice(ratings)
    
    #Parse string
    toRate = h.parse(message.content)

    if len(toRate) == 0: #Nothing to rate
        return h.badArgs("rate")
    elif len(toRate) > 1: #Too many things to rate
        return "I can only rate one thing!"

    for i in set(toRate): toRate = i #Change back to string

    if toRate.upper() in {
        "FUNKYBOT","FUNKY","YOU"}:
        return "I give myself an 11/10. Literally the best ever." 
    else:
        if toRate.upper() in {"ME","MYSELF"}:
            toRate = message.author.display_name
        return ("I give %s a %s out of 10. %s" %
                (toRate, rank.find("rank").text, rank.find("descriptor").text))
