#==== Imports ====
import discord
import asyncio
from funktions import helpers, constant
from messenger import (information_messenger as i,
                       useful_messenger as u,
                       fun_messenger as f)

#==== Definitions ====
client = discord.Client()
token = None
apiHeaders = None
with open(helpers.filePath("lists/blacklist.txt"), 'r') as o: #Load blacklist
    #Updating the blacklist requires restarting FunkyBot
    blacklist = o.readlines()
begin = helpers.getTime() #Time when Funky begins running

#==== Get user information ====
def getUserInfo():
    #This whole method feels wrong
    global token
    global apiHeaders
    
    root = helpers.getXmlTree("userinfo")
    token = root.find("token").text
    apiHeaders = {'User-Agent': root.find("user-agent").text,
                  'From': root.find("email").text }

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
        await i.hello(message,begin)

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

    elif message.content.upper().startswith('!JOKE'):
        await f.joke(message)

    elif message.content.upper().startswith('!REACT'):
        await f.react(message)

    elif message.content.upper().startswith('!RATE'):
        await f.rate(message)

    elif message.content.upper().startswith('!SHIBE'):
        await f.shibe(message)
        
#==== Begin FunkyBot ====
getUserInfo()

client.run(token)
