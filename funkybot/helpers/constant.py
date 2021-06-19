#==== Description ====
"""
Contains constants
"""

VERSION = "2.0.1"

HELP_REMINDER = "If you need specific information on commands or general use, send the `!help` command with the command you want help with. For example, `!help [!ask]`."

POLL_START = "To vote in this poll, click on the reaction corresponding to the option you want to vote for. This poll will run for %s. %s, if you would like to end this poll early send `!end`."

POLL_END = "%s's poll is over! Here are the results: %s"

REMIND_CONFIRM_1 = "Ok %s, I will remind you in %s with the following message:\n\n"

REMIND_CONFIRM_2 = "If that is ok, reply with `!yes`. If not, reply with `!no`."

ANNOUNCE_CONFIRM_1 = "Ok %s, I will remind everyone in %s with the following message:\n\n"

HELLO = "Hello %s, my name is FunkyBot! I am a simple bot made for fun as my creator's personal project. Here's some information about me:"

HELLO_HELP = "For a list of commands, send '!help'."

HELLO_URL = "https://github.com/JamesNiedfeldt/FunkyBot"

HELLO_CHANGELOG = "[Click here](https://github.com/JamesNiedfeldt/FunkyBot/wiki/Changelog) to see all of the v{} changes in greater detail.".format(VERSION)

BAD_ARGS_1 = "I couldn't understand your command!\n\n"

BAD_ARGS_2 = "If you need more help with this command, send `!help [!%s]`."

LINE_BREAK = "\n--------------------\n"

UNKNOWN_COMMAND = "Sorry, `!%s` is not one of my commands. Send `!help` for a full list."

SUGGESTED_COMMAND = "Did you perhaps mean `!%s`? If so, send `!yes` within 15 seconds to use that command."

RETRY_EQUATION = "Make sure your equation is right and try again."

CHECK_CONFIG = " Check /files/funkybot.conf."

BAD_PROPERTY_BLANK = "ERROR LOADING CONFIG: %s property must not be left blank." + CHECK_CONFIG

BAD_PROPERTY_BOOL = "ERROR LOADING CONFIG: %s property may only be \"true\" or \"false\"." + CHECK_CONFIG 

BAD_PROPERTY_INT = "ERROR LOADING CONFIG: %s property may only be an integer between %s and %s." + CHECK_CONFIG

BAD_PROPERTY_MAGIC = "ERROR LOADING CONFIG: magic_currency property may only be \"usd\", \"eur\", or \"tix\"." + CHECK_CONFIG

BAD_PROPERTY_GAME = "ERROR LOADING CONFIG: giantbomb_token must not be blank if !game command is enabled." + CHECK_CONFIG

CANT_BOOT = "ERROR STARTING FUNKYBOT: Could not verify properties."

BOOT_UP = """===============
%s %s
I'm ready to work!"""

#Common mistaken command names, to be updated as they become apparent
COMMON_MISTAKES = {
        '!bin': '!binary',
        '!math': '!calc',
        '!choice': '!choose',
        '!shibe': '!cute',
        '!mtg': '!magic',
        '!card': '!magic',
        '!vote': '!poll'}
