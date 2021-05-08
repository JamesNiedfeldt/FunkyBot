#==== Description ====
"""
Contains the informational FunkyBot commands
"""

#==== Imports ====
import re

from helpers import (helper_functions as h,
                     constant as c,
                     global_vars as g)
from helpers.objects import embeddable
from errors import errors

#==== Introduce FunkyBot ====
def sayHello():
    txt = ("**Uptime:**\n%s" % h.formatTime(h.getTime(),offset=g.begin)
           + c.LINE_BREAK
           + "**Latest changes:**")
    
    changeList = h.getXmlTree('changelogs').find("./version/[@num='{}']".format(c.VERSION))
    if changeList is None:
        txt = txt + "\n*No changes were found.*"
    else:
        for change in changeList.findall('change'):
            txt = txt + "\n\N{BULLET} %s\n" % change.text
    
    emb = embeddable.Embeddable(url=c.HELLO_URL,
                                title="FunkyBot v%s" % c.VERSION,
                                text=txt,
                                footer=c.HELLO_HELP)

    return emb

#==== Send a help message ====
def sendHelp(message):
    cmdList = h.getXmlTree('commands')
    toReturn = ""

    #No attempted arguments sent, so send list of commands
    if re.search("\[|\]", message.content) == None:
        toReturn = "Here are my commands:\n"
        info = "**Information:**"
        useful = "**Useful:**"
        fun = "**Fun:**"

        for cmd in cmdList.findall("./function"):
            if not h.isDisabled(cmd.find("command").text):
                if cmd.get("category") == "information":
                    info = info + " `{}`".format(cmd.find("format").text)
                elif cmd.get("category") == "useful":
                    useful = useful + " `{}`".format(cmd.find("format").text)
                elif cmd.get("category") == "fun":
                    fun = fun + " `{}`".format(cmd.find("format").text)

        toReturn = (toReturn + h.blockQuote(info)
                    + h.blockQuote(useful) + h.blockQuote(fun)
                    + "\n" + c.HELP_REMINDER)

    else:
        try:
            #Specific request
            arg = h.parseArgs(message.content, "help", 1, 1)
            
            for i in set(arg): arg = i.lower() #Change back to string
            if(arg.startswith("!")):
                arg = arg[1:]

            cmd = cmdList.find("./function/[command='{}']".format(arg))
            if cmd == None:
                raise errors.CustomCommandException("help", "bad_command")
            elif h.isDisabled(cmd.find("command").text):
                toReturn = "Sorry, the command you're trying to find help for is disabled."
            else:
                toReturn = "Here's how to use `!{}`:\n".format(cmd.find("command").text)
                for b in cmd.findall("body"):
                    toReturn = toReturn + "\n" + b.find("description").text + "\n"
                    for i in b.findall("hint"):
                        toReturn = toReturn + h.blockQuote(
                            "\N{BULLET} " + h.formatProps(cmd.find("command").text, i.text))
                        
        except errors.Error as e:
            raise e

    return toReturn

