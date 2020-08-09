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
    arg = h.parse(message.content)
    cmdList = h.getXmlTree('commands')
    toReturn = ""

    #No specific request
    if len(arg) == 0:
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

    #Too many commands
    elif len(arg) > 1:
        toReturn = "I can only help you with one command at a time!"

    #Specific request
    else:
        for i in set(arg): arg = i.lower() #Change back to string
        if(arg.startswith("!")):
            arg = arg[1:]

        cmd = cmdList.find("./function/[command='{}']".format(arg))
        if cmd == None:
            return ("I don't have the command you're asking for." +
                    "\n\nIf you need a list of commands, send `!help` with no options.")
        else:
            toReturn = "Here's how to use `!{}`:\n".format(cmd.find("command").text)
            for b in cmd.findall("body"):
                toReturn = toReturn + "\n" + b.find("description").text + "\n"
                for i in b.findall("hint"):
                    toReturn = toReturn + h.blockQuote(" - " + i.text)

    return toReturn

