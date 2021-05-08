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
    globs.begin = helpers.getTime()
    print((constant.BOOT_UP) % (globs.client.user.name, constant.VERSION) + "\n")
    
    await globs.client.change_presence(activity=discord.Game("!help"))
    helpers.startReminders()
    helpers.logStartup()
    print("Number of reminders from DB: %s" % helpers.getNumReminders())

#==== Listen to commands ====
@globs.client.event
async def on_message(message):
    try:
        if message.author == globs.client.user: #Do not refer to self
            return
        elif str(message.author.id) in globs.denylist: #User not allowed to use Funky
            return

        #Check if a command exists, and if not, suggest one
        if message.content.startswith('!'):
            corrected = False #Only used for commands that delete messages
            cmd = message.content.split(' ',1)[0].lower()[1:]
            expected = helpers.parseCommand(cmd)
            
            if cmd != expected:
                corrected = True
                suggestion = (constant.UNKNOWN_COMMAND % cmd + "\n\n" +
                              constant.SUGGESTED_COMMAND % expected)
                def pred(msg):
                    return (msg.author == message.author and
                            msg.channel == message.channel)

                try:
                    await message.channel.send(suggestion)
                    reply = await globs.client.wait_for('message', check=pred, timeout=15)
                    if reply.content.lower().startswith('!yes'):
                        cmd = expected
                    else:
                        return
                except asyncio.TimeoutError:
                    return
        else:
            return

        #Check if command is enabled
        if helpers.isDisabled(cmd):
            await message.channel.send("Sorry, that command is disabled.")

        #Information commands
        elif cmd == 'hello':
            await i.hello(message)

        elif cmd == 'help':
            await i.help(message)

        #Useful commands
        elif cmd == 'announce':
            await u.announce(message)

        elif cmd == 'binary':
            await u.binary(message)

        elif cmd == 'calc':
            await u.calc(message)

        elif cmd == 'hex':
            await u.hexadec(message)

        elif cmd == 'magic':
            await u.magic(message)

        elif cmd == 'poll':
            await u.poll(message)

        elif cmd == 'remind':
            await u.remind(message, time=False)

        elif cmd == 'roll':
            await u.roll(message)

        elif cmd == 'time':
            await u.remind(message, time=True)

        elif cmd == 'wiki':
            await u.wiki(message)

        #Fun commands
        elif cmd == 'ask':
            await f.ask(message)

        elif cmd == 'choose':
            await f.choose(message)

        elif cmd == 'cute':
            await f.cute(message, corrected)

        elif cmd == 'joke':
            await f.joke(message)

        elif cmd == 'react':
            await f.react(message, corrected)

        elif cmd == 'rate':
            await f.rate(message)

    except Exception as e:
        #If an exception makes it all the way here, output it to a log file
        helpers.logException(e)

globs.client.run(globs.props['token'])
