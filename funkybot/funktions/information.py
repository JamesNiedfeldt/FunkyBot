#==== Description ====
"""
Contains the informational FunkyBot commands
"""

from funktions import helpers as h
from funktions import constant as c
import re

#==== Introduce FunkyBot ====
def sayHello(sender,uptime):
    return ((c.HELLO % sender.display_name) + "\n" +
            h.blockQuote("**Current version:** %s" % c.VERSION) +
            h.blockQuote("**Current uptime:** %s" % h.formatTime(h.getTime(),offset=uptime)))

#==== Send a help message ====
def sendHelp(message):
    #Parse command
    arg = h.parse(message.content)
    cmdList = h.getXmlTree('commands')
    toReturn = ""

    if arg == None:
        if re.search("\[|\]", message.content) == None: #List of commands
            toReturn = "Here are my commands:\n"

            info = "**Information:**"
            useful = "**Useful:**"
            fun = "**Fun:**"

            for cmd in cmdList.findall("./function"):
                if cmd.get("category") == "information":
                    info = info + " `{}`".format(cmd.find("format").text)
                elif cmd.get("category") == "useful":
                    useful = useful + " `{}`".format(cmd.find("format").text)
                elif cmd.get("category") == "fun":
                    fun = fun + " `{}`".format(cmd.find("format").text)

            toReturn = (toReturn + h.blockQuote(info)
                        + h.blockQuote(useful) + h.blockQuote(fun)
                        + "\n" + c.HELP_REMINDER)
            
        else: #Arguments not formatted properly for specific request
            toReturn = h.badArgs("help", c.ERR_BRACKETS)
           
    elif len(arg) == 0: #Nothing to find
        toReturn = h.badArgs("help", c.ERR_TOO_FEW)
    elif len(arg) > 1: #Too many commands
        toReturn = h.badArgs("help", c.ERR_TOO_MANY)

    #Specific request
    else:
        for i in set(arg): arg = i.lower() #Change back to string
        if(arg.startswith("!")):
            arg = arg[1:]

        cmd = cmdList.find("./function/[command='{}']".format(arg))
        if cmd == None:
            toReturn = h.badArgs("help", "bad_command")
        else:
            toReturn = "Here's how to use `!{}`:\n".format(cmd.find("command").text)
            for b in cmd.findall("body"):
                toReturn = toReturn + "\n" + b.find("description").text + "\n"
                for i in b.findall("hint"):
                    toReturn = toReturn + h.blockQuote(" - " + i.text)

    return toReturn

