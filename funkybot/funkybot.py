#==== Imports ====
import discord
import asyncio

from helpers import (constant,
                     helper_functions as helpers,
                     global_vars as globs)
from messenger import (information_messenger as i,
                       useful_messenger as u,
                       fun_messenger as f)

#==== Begin FunkyBot ====
helpers.initGlobals(discord.Client())

#==== Alert that Funky is ready ====
@globs.client.event
async def on_ready():
    helpers.logStartup()
    print((constant.BOOT_UP) % (globs.client.user.name, constant.VERSION) + "\n")
    print("Number of reminders from DB: %s" % helpers.getNumReminders())
    
    await globs.client.change_presence(activity=discord.Game("!help"))

#==== Listen to commands ====
@globs.client.event
async def on_message(message):
    try:
        if message.author == globs.client.user: #Do not refer to self
            pass
        elif str(message.author.id) in globs.denylist: #User not allowed to use Funky
            pass

        #Information commands
        elif message.content.upper().startswith('!HELLO'):
            await i.hello(message)

        elif message.content.upper().startswith('!HELP'):
            await i.help(message)

        #Useful commands
        elif message.content.upper().startswith('!ANNOUNCE'):
            await u.announce(message)

        elif message.content.upper().startswith('!BINARY'):
            await u.binary(message)

        elif message.content.upper().startswith('!CALC'):
            await u.calc(message)

        elif message.content.upper().startswith('!HEX'):
            await u.hexadec(message)

        elif message.content.upper().startswith('!MAGIC'):
            await u.magic(message)

        elif message.content.upper().startswith('!POLL'):
            await u.poll(message)

        elif message.content.upper().startswith('!REMIND'):
            await u.remind(message)

        elif message.content.upper().startswith('!ROLL'):
            await u.roll(message)

        elif message.content.upper().startswith('!WIKI'):
            await u.wiki(message)

        #Fun commands
        elif message.content.upper().startswith('!ASK'):
            await f.ask(message)

        elif message.content.upper().startswith('!CHOOSE'):
            await f.choose(message)

        elif message.content.upper().startswith('!CUTE'):
            await f.cute(message)

        elif message.content.upper().startswith('!JOKE'):
            await f.joke(message)

        elif message.content.upper().startswith('!REACT'):
            await f.react(message)

        elif message.content.upper().startswith('!RATE'):
            await f.rate(message)

        #Attempted command doesn't exist
        elif message.content.startswith('!') and not (
            message.content.startswith('!yes') or
            message.content.startswith('!no') or
            message.content.startswith('!end')):
            await i.unknown(message)

    except Exception as e:
        #If an exception makes it all the way here, output it to a log file
        helpers.logException(e)

globs.client.run(globs.token)
