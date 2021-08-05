#==== Description ====
"""
Contains the non-command functions needed to run
"""

#==== Imports ====
from datetime import datetime, date, timezone, timedelta
import discord
import os
import re
import xml.etree.ElementTree as et
import traceback

from helpers import (constant as c,
                     global_vars as g)
from helpers.objects import reminder, database, poll
from errors import errors

#========================================
#======== User data verification ========
#========================================

#==== Parse a string ====
def parseArgs(string, command, minArg, maxArg):
    contents = re.findall("\[([^\[\]]*)\]", string)

    if len(contents) == 0: #Nothing was found
        raise errors.BadArgumentException(command)
    
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
    
    for i in contents:
        if i == "": #Is there a blank entry?
           raise errors.EmptyArgumentException(command)

    if len(contents) < minArg:
        raise errors.TooFewArgumentsException(command)
    elif len(contents) > maxArg:
        raise errors.TooManyArgumentsException(command)

    return contents

#==== Error in command arguments ====
def badArgs(exc):
    cmd = getXmlTree("commands").find("./function/[command='{}']".format(exc.command))
    message = c.BAD_ARGS_1

    if exc.errorCode != None and cmd != None:
        hint = cmd.find("./error/[@type='{}']".format(exc.errorCode))
        if hint != None:
            message = message + formatProps(exc.errorCode, hint.text) + c.LINE_BREAK

    message = message + c.BAD_ARGS_2 % exc.command

    return message

#==== Determine if a function is disabled ====
def isDisabled(cmd):
    return cmd in g.props and g.props[cmd] != 'true'

#==== Decide if a user was trying to send unknown command ====
def parseCommand(cmd):
    cmdList = getXmlTree('commands')

    for i in cmdList:
        if i.find("command").text == cmd:
            return cmd
        
    #Is it a common mistake for an enabled command?
    if cmd in g.commonMistakes and not isDisabled(g.commonMistakes[cmd]):
        return g.commonMistakes[cmd]
    #If not, find the best match
    else:
        return _lDistance(cmd, cmdList)

#==== Find Levenshtein distance between two strings ====
#https://en.wikipedia.org/wiki/Levenshtein_distance
def _lDistance(unknown, cmdList):
    bestScore = None
    toReturn = None

    for cmd in cmdList.findall('./function'):
        if cmd.get("category") != "contextual":
            mat = []
            target = cmd.find("command").text

            if isDisabled(target):
                continue
    
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
                    if unknown[i - 1] == target[j - 1]: #Perfect match
                        subCost = 0
                    elif unknown[i - 1] in target[j:]: #Match later
                        subCost = 1
                    elif unknown[i - 1] in target[:j]: #Match earlier
                        subCost = 1
                    else: #No match
                        subCost = 2
                        
                    mat[i][j] = min(mat[i-1][j] + 1,
                                  mat[i][j-1] + 1,
                                  mat[i-1][j-1] + subCost)
                    j = j + 1
                i = i + 1

            if bestScore == None or mat[len(unknown)][len(target)] < bestScore:
                bestScore = mat[len(unknown)][len(target)]
                toReturn = target
        
    return toReturn

#================================
#======== File functions ========
#================================
    
#==== Log deleted messages ====
def logMessage(message):
    with open(filePath('logs/'+str(message.guild)+'-deletions.log'),'a+', encoding='utf-8') as log:
        toLog = "%s - %s - %s: %s\n" % (message.created_at.strftime("%Y-%b-%d %H:%M"),message.channel,message.author.name,message.content)
        log.write(toLog)

#==== Check directories for valid images ====
def validFolder(files):
    if len(files) > 1:
        return True
    else:
        return False

#==== Return relative path ====
def filePath(directory):
    absolute = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(absolute, "files/" + directory)
    return path

#==== Grab a root XML tree from a file ====
def getXmlTree(fileName):
    tree = et.parse(filePath('xml/{}.xml'.format(fileName)))
    return tree.getroot()

#==== Log startup ====
def logStartup():
    with open(filePath("logs/funkybot-%s.log" % date.today()), 'a+') as f:
        f.write(c.LINE_BREAK + "Starting session at {}\n".format(
            datetime.fromtimestamp(g.begin)))
        f.write("Number of reminders from DB: {}\n".format(getNumReminders()))

#==== Log exceptions ====
def logException(e):
    with open(filePath("logs/funkybot-%s.log" % date.today()), 'a+') as f:
        f.write('\n')
        traceback.print_exc(file=f)

#==== Log command use into db ====
def logCommand(cmd):
    g.db.incrementCommand(cmd)

#==== Get command usage stats ====
def getTopCommands():
    return g.db.getTopCommands()

#=========================================
#======== Global var manipulation ========
#=========================================

#==== Check if randomized image was recently used ====
def duplicateImage(img, path):
    if path == 'cute_pics':
        return img in g.recentCute
    elif path == 'reaction_pics':
        return img in g.recentReact
    else:
        return False

#==== Add image to recently used randomized images ====
def updateDuplicateImages(img, path):
    if path == 'cute_pics':
        g.recentCute.append(img)
        if len(g.recentCute) > 5:
            g.recentCute.pop(0)
    elif path == 'reaction_pics':
        g.recentReact.append(img)
        if len(g.recentReact) > 5:
            g.recentReact.pop(0)

#==== Check if a poll is already being run by someone ====
def isPollRunning(poll):
    return poll.activeId in g.activePolls

#==== Add an ID to active running polls ====
def addToActivePolls(poll):
    g.db.insertPoll(poll)

#==== Remove an ID from active running polls ====
def removeFromActivePolls(poll):
    g.db.deletePoll(poll)

#==== Return number of reminders running ====
def getNumReminders():
    return len(g.reminders)

#==== Initalize global variables ====
def initGlobals(client):
    g.client = client
    g.begin = getTime()

    __readConfig() #Get properties from funkybot.conf
    __verifyProps() #Check if FunkyBot is ok to load with set properties
    g.apiHeaders = {'User-Agent': g.props['request_name'],
                  'From': g.props['request_email'] }

    root = getXmlTree("denylist")
    for u in root.findall("user"):
        g.denylist.append(u.text)

    root = getXmlTree("common_mistakes")
    for m in root.findall("command"):
        g.commonMistakes[m.text] = m.get("suggestion")

    g.db = database.Database()

    if g.props['reset_command_usage'] == 'true':
        g.db.clearCommands()

#==== Start reminders from database ====
def startReminders():
    g.db.loadReminders()    
    for r in g.reminders:
        r.beginThread()

#==== Unpin dead polls and clear them from database ====
async def clearDeadPolls():
    idPairs = g.db.clearDeadPolls()

    if idPairs != None:
        try:
            for m in idPairs:
                channel = g.client.get_channel(idPairs[m])
                message = await channel.fetch_message(m)
                await message.unpin(reason="Poll can't be finished")
        except discord.errors.Forbidden: #Can't unpin
            pass
                
#================================
#======== Time functions ========
#================================

#==== Get current time ====
def getTime():
    return datetime.now().timestamp()

#==== Format uptime ====
def formatTime(time,offset=0):
    totalSec = int(time - offset)

    if totalSec < 0:
        return "Error: Invalid time"

    seconds = totalSec % 60
    minutes = int((totalSec % 3600) / 60)
    hours = int((totalSec % 86400) / 3600)
    days = int(totalSec / 86400)

    formatted = (pluralize(days, "day") + ", " +
                 pluralize(hours, "hour") + ", " +
                 pluralize(minutes, "minute") + ", and " +
                 pluralize(seconds, "second") + ".")

    return formatted

#==== Convert reminder arguments to duration ====
def convertDurationTime(timeArgs):
    duration = 0
         
    for i in timeArgs:
        key = re.findall("[smhd]", i, flags=re.IGNORECASE)

        try:
            if len(key) is 0:
                return None
            else:
                num = float(re.split(key[0] ,i)[0])
                if num < 0:
                    raise errors.CustomCommandException('time', 'negative_time')
                key = key[0].lower()

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
    try:
        tokens = timeArgs[0].split()

        tzOffset = tokens[-1]
        tz = timezone(timedelta(hours=float(tzOffset)))
        
        if '/' in tokens[0]: #First token is a date
            datePcs = [int(i) for i in tokens[0].split('/')]
            if len(str(datePcs[2])) == 2: #2 digit year
                datePcs[2] = datePcs[2] + 2000
            tokens = tokens[1:]
        else:
            datePcs = datetime.now(tz)
            datePcs = [datePcs.month, datePcs.day, datePcs.year]

        time = [int(i) for i in tokens[0].split(':')]
        if tokens[1].lower() == 'pm':
            if time[0] < 12:
                time[0] = time[0] + 12
        elif tokens[1].lower() == 'am':
            if time[0] == 12:
                time[0] = time[0] - 12

        calculatedDt = datetime(
            datePcs[2], datePcs[0], datePcs[1],
            hour=time[0], minute=time[1], tzinfo=tz)

        if calculatedDt.timestamp() <= getTime():
            return -1
        else:
            return calculatedDt.timestamp()
        
    except:
        return None

#=====================================
#======== String manipulation ========
#=====================================

#==== Format string to use block quotes ====
def blockQuote(string):
    return "> " + string + "\n"

#==== Format a help string with property values ====
def formatProps(cmd, string):
    props = {
        'roll_max_args': pluralize(g.props['roll_max_args'], "die"),
        'choose_max_args': g.props['choose_max_args'],
        'binary_max_args': pluralize(g.props['binary_max_args'], "number"),
        'hex_max_args': pluralize(g.props['hex_max_args'], "number"),
        'time_max_duration': pluralize(g.props['time_max_duration'], "day"),
        'poll_max_duration': pluralize(g.props['poll_run_duration'], "hour")}
    
    return string.format(**props)

#==== Pluralize a string if necessary ====
def pluralize(num, string):
    if int(num) != 1:
        if string.lower() == "die":
            return str(num) + " dice"
        else:
            toReturn = str(num) + " " + string
            if string[-1] == 's' or string[-2:] == "sh":
                return toReturn + "es"
            return toReturn + "s"
    else:
        return str(num) + " " + string

#=======================================
#======== Property verification ========
#=======================================

#==== Read the config file ====
def __readConfig():
    with open(filePath("funkybot.conf")) as f: 
        for line in f:
            ln = line.strip()
            if not ln.startswith("#") and ln != "":
                pair = ln.split("=")
                g.props[pair[0].strip()] = pair[1].strip()

#==== Verify properties ====
def __verifyProps():
    expectedProps = getXmlTree("expected_properties").findall("./property")

    try:
        for prop in expectedProps:
            if prop.text == "giantbomb_key":
                if (('game' not in g.props or g.props['game'] == 'true')
                    and g.props['giantbomb_key'] == ''):
                    raise RuntimeError(c.BAD_PROPERTY_GAME)
                
            elif prop.text == "magic_currency":
                if (('magic' not in g.props or g.props['magic'] == 'true')
                    and g.props[prop.text] not in prop.get("options").split(',')):
                    raise RuntimeError(c.BAD_PROPERTY_MAGIC)
                
            else:
                if g.props[prop.text] == '':
                    raise RuntimeError(c.BAD_PROPERTY_BLANK % prop.text)
                elif prop.get("type") == "bool":
                    if g.props[prop.text] not in ('true', 'false'):
                        raise RuntimeError(c.BAD_PROPERTY_BOOL % prop.text)
                elif prop.get("type") == "int":
                    if (int(g.props[prop.text]) < int(prop.get("min")) or
                        int(g.props[prop.text]) > int(prop.get("max"))):
                        raise RuntimeError(c.BAD_PROPERTY_INT % (prop.text, prop.get("min"), prop.get("max")))
                

    except RuntimeError:
        print(c.CANT_BOOT)
        raise
    except KeyError:
        print(c.CANT_BOOT)
        raise
