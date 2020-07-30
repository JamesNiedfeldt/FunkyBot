#==== Imports ====
import discord
import asyncio
from funktions import helpers, constant
from messenger import information, useful, fun

#==== Definitions ====
client = discord.Client()
with open(helpers.filePath("lists/blacklist.txt"), 'r') as o: #Load blacklist
    #Updating the blacklist requires restarting FunkyBot
    blacklist = o.readlines()
begin = helpers.getTime() #Time when Funky begins running

#==== Alert that Funky is ready ====
@client.event
async def on_ready():
    print((constant.BOOT_UP) % (client.user.name, constant.VERSION) + "\n")
    helpers.setUpReminders(client)

#==== Listen to commands ====
@client.event
async def on_message(message):
    if message.author == client.user: #Do not refer to self
        pass
    elif message.author.id in blacklist: #User not allowed to use Funky
        pass

    #Information commands
    elif message.content.upper().startswith('!HELLO'):
        await information.hello(message,begin)

    elif message.content.upper().startswith('!HELP'):
        await information.help(message)

    #Useful commands
    elif message.content.upper().startswith('!ANNOUNCE'):
        await useful.announce(message,client)

    elif message.content.upper().startswith('!BINARY'):
        await useful.binary(message)

    elif message.content.upper().startswith('!HEX'):
        await useful.hexadec(message)

    elif message.content.upper().startswith('!MAGIC'):
        await useful.magic(message)

    elif message.content.upper().startswith('!REMIND'):
        await useful.remind(message,client)

    elif message.content.upper().startswith('!ROLL'):
        await useful.roll(message)

    elif message.content.upper().startswith('!WIKI'):
        await useful.wiki(message)

    #Fun commands
    elif message.content.upper().startswith('!ASK'):
        await fun.ask(message)

    elif message.content.upper().startswith('!CHOOSE'):
        await fun.choose(message)

    elif message.content.upper().startswith('!JOKE'):
        await fun.joke(message)

    elif message.content.upper().startswith('!REACT'):
        await fun.react(message)

    elif message.content.upper().startswith('!RATE'):
        await fun.rate(message)

    elif message.content.upper().startswith('!SHIBE'):
        await fun.shibe(message)
        
#==== Log on ====
with open(helpers.filePath("token.txt"),'r') as o:
    token = o.readline()
    client.run(token)


