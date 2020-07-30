#==== Description ====
"""
Contains the informational FunkyBot commands
"""

from funktions import helpers as h
from funktions import constant as c

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
        return ("Here are my commands:\n" +
                h.blockQuote(c.INFO_LIST) +
                h.blockQuote(c.USEFUL_LIST) +
                h.blockQuote(c.FUN_LIST) + "\n" +
                c.HELP_REMINDER)
    elif len(command) > 1: #Too many commands
        return "I can only help you with one command at a time!"
    else:
        for i in set(command): command = i #Change back to string
        if(command.startswith("!")):
            command = command[1:]
        try:
            with open(h.filePath(('help_files/%s.txt' % command.lower())), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ("I don't have the command you're asking for." +
                    "\n\nIf you need a list of commands, send `!help` with no options.")

