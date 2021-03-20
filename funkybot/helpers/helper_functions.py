#==== Description ====
"""
Contains the non-command functions needed to run
"""

#==== Imports ====
from datetime import datetime
import time
import os
import re
import xml.etree.ElementTree as et
import traceback

from helpers import constant as c
from helpers.objects import reminder, database, poll
from errors import errors

#==== Parse a string ====
def parse(string, command, minArg, maxArg):
    contents = re.findall("\[\[([^\[\]]*)\]\]", string) #Find contents of '[[]]'

    if len(contents) == 0: #Nothing was found
        raise errors.BadArgumentException(command)
    
    contents = re.split("\|", contents[0])  #Split multiple deliminated with '|'
    
    for i in list(contents):
        if i == "": #Is there a blank entry?
           raise errors.EmptyArgumentException(command)

    if len(contents) < minArg:
        raise errors.TooFewArgumentsException(command)
    elif len(contents) > maxArg:
        raise errors.TooManyArgumentsException(command)
        
    return contents
    
#==== Log deleted messages ====
def logMessage(message):
    with open(filePath('logs/'+str(message.guild)+'-log.log'),'a+', encoding='utf-8') as log:
        toLog = "%s - %s - %s: %s\n" % (message.created_at.strftime("%Y-%b-%d %H:%M"),message.channel,message.author.name,message.content)
        log.write(toLog)

#==== Check directories for valid images ====
def validFolder(files):
    if len(files) > 1:
        return True
    else:
        return False

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
def badArgs(exc):
    cmd = getXmlTree("commands").find("./function/[command='{}']".format(exc.command))
    message = c.BAD_ARGS_1

    if exc.errorCode != None and cmd != None:
        hint = cmd.find("./error/[@type='{}']".format(exc.errorCode))
        if hint != None:
            message = message + hint.text + " "

    message = message + c.BAD_ARGS_2 % exc.command

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

    return duration

#==== Convert reminder arguments to datetime ====
def convertDateTime(timeArgs):
    arg = timeArgs[0]
    
    try:
        date = datetime.strptime(arg, "%m/%d/%Y %H:%M %z")
        if date.timestamp() <= getTime():
            return -1
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

#==== Decide if a user was trying to send unknown command ====
def parseUnknown(cmd):
    result = re.match("^!{1}[\w]+", cmd)
    if result == None:
        return None

    else:
        result = result.group()[1:]
        toReturn = c.UNKNOWN_COMMAND % result
        attempted = lDistance(result)
        if attempted != None:
            toReturn = toReturn + "\n\nDid you perhaps mean `!%s`?" % attempted

        return toReturn

#==== Find Levenshtein distance between two strings ====
def lDistance(unknown):
    index = getXmlTree('commands').findall('./function')
    bestScore = None
    toReturn = None

    for cmd in index:
        if cmd.get("category") != "contextual":
            mat = []
            target = cmd.find("command").text
    
            for l in range(len(unknown) + 1):
                y = []
                for r in range(len(target) + 1):
                    y.append(0)
                mat.append(y)

            for i in range(1, len(unknown) + 1):
                mat[i][0] = i
            for i in range(1, len(target) + 1):
                mat[0][i] = i
            
            i = 1
            while i < len(mat):
                j = 1
                while j < len(mat[i]):
                    if unknown[i - 1] == target[j - 1]:
                        subCost = 0
                    else:
                        subCost = 1
                        
                    mat[i][j] = min(mat[i-1][j] + 1,
                                  mat[i][j-1] + 1,
                                  mat[i-1][j-1] + subCost)
                    j = j + 1
                i = i + 1

            if bestScore == None or mat[len(unknown)][len(target)] < bestScore:
                bestScore = mat[len(unknown)][len(target)]
                toReturn = target
        
    return toReturn

#==== Return number of reminders running ====
def getNumReminders():
    return len(database.db.reminders)

#==== Log startup ====
def logStartup(startTime):
    with open(filePath("logs/funkylog.log"), 'a+') as f:
        f.write(c.LINE_BREAK + "Starting session at {}\n".format(
            datetime.fromtimestamp(startTime)))
        f.write("Number of reminders from DB: {}\n".format(getNumReminders()))

#==== Log exceptions ====
def logException(e):
    with open(filePath("logs/funkylog.log"), 'a+') as f:
        f.write('\n')
        traceback.print_exc(file=f)
        
