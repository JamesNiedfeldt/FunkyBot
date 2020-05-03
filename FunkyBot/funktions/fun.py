#==== Description ====
"""
Contains the fun FunkyBot commands
"""

from funktions import helpers as h
import random
import os

#==== Answer a yes/no question ====
def eightBall():
    with open(h.filePath('lists/answers.txt'), 'r') as file:
        answers = file.readlines()

    return random.choice(answers)

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
    with open(h.filePath('lists/jokes.txt'), 'r') as file:
        jokes = file.readlines()

    return random.choice(jokes)

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
    with open(h.filePath('lists/ratings.txt'),'r') as file:
        ratings = file.readlines()
    score = random.randint(1, 10)
    
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
    elif toRate.upper() in {
        "ME","MYSELF"}:
        return "I give %s a %s out of 10. %s" % (message.author.display_name, score, ratings[score-1])
    else:
        return "I give %s a %s out of 10. %s" % (toRate, score, ratings[score-1])
