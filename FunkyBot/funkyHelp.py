#==== Description ====
"""
Acts as a database to help users with FunkyBot's commands
"""

#==== Determine how to help ====
def getHelp(command):
    #!ask
    if command.upper() in {
        "ASK", "!ASK"}:
        return("""
        Here's how to use `!ask`:\n
Send `!ask` to get a yes or no answer to something.
""")

    #!binary
    elif command.upper() in {
        "BINARY", "!BINARY"}:
        return("""
        Here's how to use `!binary`:\n
Send `!binary [[X]]` to have me convert your number to binary.
- For example, to convert 5 to binary, you should send: `!binary [[5]]`.
- I can only convert one number at a time and no numbers higher than 1024.
""")

    #!commands
    elif command.upper() in {
        "COMMANDS", "!COMMANDS"}:
        return("""
        Here's how to use `!commands`:\n
Send `!commands` to see a list of available commands for me.
""")

    #!choose
    elif command.upper() in {
        "CHOOSE", "!CHOOSE"}:
        return("""
        Here's how to use `!choose`:\n
Send `!choose [[X|Y|...]]` to have me choose from your options.
- For example, to choose from cats or dogs, you should send: `!choose [[cats|dogs]]`.
- I need at least two choices to choose from, but you can send up to ten.
- Make sure you separate each choice by using the | character.
""")

    #!hello
    elif command.upper() in {
        "HELLO", "!HELLO"}:
        return("""
        Here's how to use `!hello`:\n
Send `!hello` to see some information about me.
- Using this command, you can get a quick description as well as see my version number and the time I've been working.
""")

    #!help
    elif command.upper() in {
        "HELP", "!HELP"}:
        return("""
        Here's how to use `!help`:\n
This is the command you're using! Send `!help [[X]]` to have me explain a command in detail.
- For example, to get an explanation of the `!binary` command, you should send: `!help [[!binary]]`.
- You can also send just the name of the command without the ! character.
- I can only send an explanation of one command at a time.
- For commands with options in double brackets, you just need to send the name of the command. Don't send any brackets.
""")

    #!hex
    elif command.upper() in {
        "HEX", "!HEX"}:
        return("""
        Here's how to use `!hex`:\n
Send `!hex [[X]]` to have me convert your number to hexadecimal.
- For example, to convert 5 to hexadecimal, you should send: `!hex [[5]]`.
- I can only convert one number at a time and no numbers higher than 65535.
""")

    #!joke
    elif command.upper() in {
        "JOKE", "!JOKE"}:
        return("""
        Here's how to use `!joke`:\n
Send `!joke` to have me send a one-liner joke. Laughs are not guaranteed.
""")

    #!magic
    elif command.upper() in {
        "MAGIC", "!MAGIC"}:
        return("""
        Here's how to use `!magic`:\n
Send `!magic [[X]]` to have me search for a Magic: The Gathering card.
- For example, to search for Island, you should send: `!magic [[island]]`.
- I can search for up to three cards, just make sure they are all in the same double brackets and separate them with the | character.
""")

    #!react
    elif command.upper() in {
        "REACT", "!REACT"}:
        return("""
        Here's how to use `!react`:\n
Send `!react` to have me send a random reaction image.
- If I am allowed to delete messages, the message you send will be deleted and its contents logged on my server.
""")

    #!rate
    elif command.upper() in {
        "RATE", "!RATE"}:
        return("""
        Here's how to use `!rate`:\n
Send `!rate [[X]]` to have me rate something on a scale from 1 to 10.
- For example, to rate Discord, you should send: `!rate [[discord]]`.
- I can only rate one thing at a time.
""")

    #!roll
    elif command.upper() in {
        "ROLL", "!ROLL"}:
        return("""
        Here's how to use `!roll`:\n
Send `!roll [[X]]` to have me roll a die.
- For example, to roll a 6-sided die, you should send: `!roll [[6]]`.
- I can only roll one die at a time.
- The die must have at least 2 sides (I guess that's just a coin?) and can have up to 1000 sides.
""")

    #!shibe
    elif command.upper() in {
        "SHIBE", "!SHIBE"}:
        return("""
        Here's how to use `!shibe`:\n
Send `!shibe` to have me send a random picture of a shiba inu.
""")
