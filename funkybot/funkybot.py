#==== Imports ====
import discord
import asyncio

from helpers import constant, helper_functions as helpers
from messenger import (information_messenger as i,
                       useful_messenger as u,
                       fun_messenger as f)

#==== Definitions ====
client = discord.Client()
token = None
apiHeaders = None
begin = helpers.getTime()
denylist = []

#==== Alert that Funky is ready ====
@client.event
async def on_ready():
    helpers.setUpReminders(client)
    helpers.logStartup(begin)
    print((constant.BOOT_UP) % (client.user.name, constant.VERSION) + "\n")
    print("Number of reminders from DB: %s" % helpers.getNumReminders())
    
    await client.change_presence(activity=discord.Game("!help"))

#==== Listen to commands ====
@client.event
async def on_message(message):
    try:
        if message.author == client.user: #Do not refer to self
            pass
        elif str(message.author.id) in denylist: #User not allowed to use Funky
            pass

        #Information commands
        elif message.content.upper().startswith('!HELLO'):
            await i.hello(message,begin,client)

        elif message.content.upper().startswith('!HELP'):
            await i.help(message)

        #Useful commands
        elif message.content.upper().startswith('!ANNOUNCE'):
            await u.announce(message,client)

        elif message.content.upper().startswith('!BINARY'):
            await u.binary(message)

        elif message.content.upper().startswith('!HEX'):
            await u.hexadec(message)

        elif message.content.upper().startswith('!MAGIC'):
            await u.magic(message,apiHeaders)

        elif message.content.upper().startswith('!POLL'):
            await u.poll(message,client)

        elif message.content.upper().startswith('!REMIND'):
            await u.remind(message,client)

        elif message.content.upper().startswith('!ROLL'):
            await u.roll(message)

        elif message.content.upper().startswith('!WIKI'):
            await u.wiki(message,apiHeaders)

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
        elif message.content.startswith('!'):
            await i.unknown(message)

    except Exception as e:
        #If an exception makes it all the way here, output it to a log file
        helpers.logException(e)
        
#==== Begin FunkyBot ====
root = helpers.getXmlTree("userinfo")
token = root.find("token").text
apiHeaders = {'User-Agent': root.find("user-agent").text,
              'From': root.find("email").text }

root = helpers.getXmlTree("denylist")
for u in root.findall("user"):
    denylist.append(u.text)

del root #No more use for this

client.run(token)
