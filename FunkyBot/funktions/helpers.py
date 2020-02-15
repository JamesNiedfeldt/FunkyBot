#==== Description ====
"""
Contains the non-command functions needed to run
"""

import time
from reminder import reminder, database
from funktions import constant as c
import os
import re

#==== Parse a string ====
def parse(string):
    contents = re.findall("\[\[([^\[\]]*)\]\]", string) #Find contents of '[[]]'
    
    if len(contents) == 0: #Nothing was found
        contents.clear()
        return contents
    
    contents = re.split("\|", contents[0])  #Split multiple deliminated with '|'
    
    for i in list(contents):
        if i == "": #Is there a blank entry?
           contents.clear()
           pass
    return contents
    
#==== Log deleted messages ====
def logMessage(message):
    with open(filePath('logs/'+str(message.guild)+'-log.txt'),'a+', encoding='utf-8') as log:
        toLog = "%s - %s - %s: %s\n" % (message.created_at.strftime("%Y-%b-%d %H:%M"),message.channel,message.author.name,message.content)
        log.write(toLog)

#==== Check directories for valid images ====
def validFolder(files):
    if len(files) > 1:
        return
    else:
        raise RuntimeError

#==== Calculate uptime ====
def getTime():
    return time.time()

#==== Format uptime ====
def formatTime(time,offset=0):
    totalSec = int(time - offset)

    if totalSec < 0:
        return "Error: Invalid time"

    seconds = totalSec % 60
    minutes = int((totalSec % 3600) / 60)
    hours = int((totalSec % 86400) / 3600)
    days = int(totalSec / 86400)

    formatted = "%s days, %s hours, %s minutes, and %s seconds" % (days, hours, minutes, seconds)

    return formatted

#==== Return relative path ====
def filePath(directory):
    absolute = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(absolute, directory)
    return path

#==== Error in command arguments ====
def badArgs(command):
    message = (c.BAD_ARGS % command)
    return message

#==== Setup and pull from reminder database at startup ====
def setUpReminders(client):
    reminder.client = client
    database.db.runThreads()

#==== Format string to use block quotes ====
def blockQuote(string):
    return "> " + string + "\n"

#==== Format Magic card information ====
def formatMagic(card, transform=False):
    textBox = (card['type_line'])

    if 'card_faces' in card and card['layout'] != "transform": #Split or other weird card
        for f in card['card_faces']:
            textBox = (textBox + "\n\n" + f['name'] + "   " + f['mana_cost'] +
                       "\n" + f['type_line'] +
                       "\n" + f['oracle_text'])
            if 'power' in f and 'toughness' in f:
                if f['power'] == '*' and f['toughness'] == '*':
                    textBox = textBox + '\n\\' + f['power'] + '/\\' + f['toughness']
                else:      
                    textBox = textBox + '\n' + f['power'] + '/' + f['toughness']

    else:
        textBox = textBox + "\n\n" + card['oracle_text']
        if 'power' in card and 'toughness' in card:
            if card['power'] == '*' and card['toughness'] == '*':
                textBox = textBox + '\n\\' + card['power'] + '/\\' + card['toughness']
            else:      
                textBox = textBox + '\n' + card['power'] + '/' + card['toughness']

    nameAndCost = card['name'] + "   " + card['mana_cost']

    if transform:
        return ([nameAndCost,
                 card['image_uris']['normal'],
                 textBox])
    
    else: 
        return ([card['scryfall_uri'],
                 nameAndCost,
                 card['image_uris']['normal'],
                 textBox])
