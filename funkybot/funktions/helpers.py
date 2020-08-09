#==== Description ====
"""
Contains the non-command functions needed to run
"""

from datetime import datetime
from reminder import reminder, database
from funktions import constant as c
from poll import poll
import time
import os
import re
import xml.etree.ElementTree as et

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
    path = os.path.join(absolute, "files/" + directory)
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

#==== Convert reminder arguments to duration ====
def convertDurationTime(timeArgs):
    duration = 0

    if len(timeArgs) > 3:
        timeArgs = timeArgs[0:3]
                
    for i in timeArgs:
        key = re.findall("[smhd]", i, flags=re.IGNORECASE)
        
        if len(key) is 0:
            return None
        else:
            num = re.split(key[0] ,i)[0]
            key = key[0].lower()

        try:
            if num == "":
                pass
            elif key == 's':
                duration = duration + float(num)
            elif key == 'm':
                duration = duration + float(num)*60
            elif key == 'h':
                duration = duration + float(num)*3600
            elif key == 'd':
                duration = duration + float(num)*86400
        except ValueError:
            return None

    #Max of 30 days
    if(duration > 2592000):
        duration = 2592000
    elif(duration <= 0):
        return None
  
    return duration

#==== Convert reminder arguments to datetime ====
def convertDateTime(timeArgs):
    arg = timeArgs[0]
    
    try:
        date = datetime.strptime(arg, "%m/%d/%Y %H:%M %z")
        if date.timestamp() <= getTime():
            return None
        else:
            return date.timestamp()
    except ValueError:
        return None

#==== Check if a poll is already being run by someone ====
def isPollRunning(activeId):
    return activeId in poll.activePolls

#==== Add an ID to active running polls ====
def addToActivePolls(activeId):
    poll.activePolls.append(activeId)

#==== Remove an ID from active running polls ====
def removeFromActivePolls(activeId):
    poll.activePolls.remove(activeId)

#==== Grab a root XML tree from a file ====
def getXmlTree(fileName):
    tree = et.parse(filePath('{}.xml'.format(fileName)))
    return tree.getroot()
