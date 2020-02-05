#==== Description ====
"""
Contains the informational FunkyBot commands
"""

from funktions import helpers as h
from funktions import constant as c

#==== Get a list of commands ====
def commandList():
    return ("Here are some of my commands:\n" +
            h.blockQuote(c.INFO_LIST) +
            h.blockQuote(c.USEFUL_LIST) +
            h.blockQuote(c.FUN_LIST) +
            c.HELP_REMINDER)

#==== Introduce FunkyBot ====
def sayHello(sender,uptime):
    return ((c.HELLO % sender.display_name) + "\n" +
            h.blockQuote("**Current version:** %s" % c.VERSION) +
            h.blockQuote("**Current uptime:** %s" % h.formatTime(h.getTime(),offset=uptime)))

#==== Send a help message ====
def sendHelp(message):
    #Parse command
    command = h.parse(message.content)

    if len(command) == 0: #Nothing to help with
        return h.badArgs("help") + "\n\nIf you need a list of commands, send `!commands`."
    elif len(command) > 1: #Too many commands
        return "I can only help you with one command at a time!"
    else:
        for i in set(command): command = i #Change back to string
        if(command.startswith("!")):
            command = command[1:]
        try:
            with open(h.filePath(('help_files/%s.txt' % command)), 'r') as file:
                toReturn = file.read()
        except FileNotFoundError:
            toReturn = h.badArgs("help") + "\n\nIf you need a list of commands, send `!commands`."
        return toReturn
