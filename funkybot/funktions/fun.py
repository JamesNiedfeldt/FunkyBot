#==== Description ====
"""
Contains the fun FunkyBot commands
"""

#==== Imports ====
import random
import os

from helpers import helper_functions as h, constant as c, global_vars as g
from errors import errors

#==== Answer a yes/no question ====
def eightBall():
    answers = h.getXmlTree("lists").findall("./list/[@type='answers']/answer")

    return random.choice(answers).text

#==== Choose randomly from choices ====
def choose(message):
    #Parse choices
    try:
        choices = h.parseArgs(message.content, "choose", 2, g.props['choose_max_args'])
    except errors.Error as e:
        raise e

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

        if not h.validFolder(pics): #Check if folder is empty
            raise RuntimeError
        while not found: #Search for a valid file path
            selection = random.choice(pics)
            
            if (selection != "Thumbs.db" and
                selection != ".gitkeep" and
                not h.duplicateImage(selection,path)):
                
                found = True
                h.updateDuplicateImages(selection,path)
                    
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
    try:
        toRate = h.parseArgs(message.content, "rate", 1, 1)
    except errors.Error as e:
        raise e

    for i in set(toRate): toRate = i #Change back to string

    if toRate.upper() in {
        "FUNKYBOT","FUNKY","YOU","YOURSELF"}:
        return "I give myself an 11/10. Literally the best ever." 
    else:
        if toRate.upper() in {"ME","MYSELF"}:
            toRate = message.author.display_name
        return ("I give %s a %s out of 10. %s" %
                (toRate, rank.find("rank").text, rank.find("descriptor").text))

#==== Play rock, paper, scissors ====
def playRps(message):
    options = {'rock': 0,
               'paper': 1,
               'scissors': 2}
    funkyChoice = random.choice(list(options))
    toReturn = "I choose **{}**!\n\n".format(funkyChoice)

    #Parse string
    try:
        playerChoice = h.parseArgs(message.content, "rps", 1, 1)[0]
    except errors.Error as e:
        raise e

    if playerChoice.lower() not in options:
        toReturn = toReturn + "{} beats...hey, you can't pick \"{}\"!".format(
            funkyChoice.capitalize(), playerChoice)
    elif options[playerChoice] == options[funkyChoice]:
        toReturn = toReturn + "It's a draw!"
    elif (options[playerChoice] + 1) % 3 == options[funkyChoice]:
        toReturn = toReturn + "{} beats {}. I win, better luck next time!".format(
            funkyChoice.capitalize(), playerChoice)
    else:
        toReturn = toReturn + "{} beats {}. You win this time!".format(
            playerChoice.capitalize(), funkyChoice)

    return toReturn

    
