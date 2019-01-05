#==== Description ====
"""
Contains the non-command functions needed to run
"""

import time
from reminder import reminder, database
import os
import re

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
    with open(filePath('logs/'+str(message.server)+'-log.txt'),'a+', encoding='utf-8') as log:
        toLog = "%s - %s - %s: %s\n" % (message.timestamp.strftime("%Y-%b-%d %H:%M"),message.channel,message.author.name,message.content)
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
    message = ("I couldn't understand your command! If you need help, send `!help [[!%s]]`." % command)
    return message

#==== Setup and pull from reminder database at startup ====
def setUpReminders(client):
    reminder.client = client
    database.db.runThreads()
