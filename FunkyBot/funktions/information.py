#==== Description ====
"""
Contains the informational FunkyBot commands
"""

from funktions import helpers as h

#==== Get a list of commands ====
def commandList():
    return("""
    Here are my commands:\n
    - **Information:** `!commands` `!hello` `!help [[X]]`
    - **Useful:** `!binary [[X]]` `!hex [[X]]` `!magic [[X|...|...]]` `!remind [[X|...]]` `!roll [[X]]`
    - **Fun:** `!ask` `!choose [[X|Y|...]]` `!joke` `!react` `!rate [[X]]` `!shibe`
\nIf you need specific information on commands or general use, send the `!help` command with the command you want help with. For example, `!help [[!ask]]`.
    """)

#==== Introduce FunkyBot ====
def sayHello(sender,version,uptime):
    return("""
    Hello %s, my name is FunkyBot! I am a simple bot made for fun as my creator's personal project. Here's some information about me:

    **Current version:** %s 
    **Current uptime:** %s 
    """ % (sender.display_name, version, h.formatTime(h.getTime(),offset=uptime)))

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
