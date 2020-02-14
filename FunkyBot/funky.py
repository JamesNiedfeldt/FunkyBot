#==== Imports ====
import discord
import asyncio
from funktions import fun, helpers, information, useful, constant

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
    author = message.author

    if author == client.user: #Do not refer to self
        pass
    elif author.id in blacklist: #User not allowed to use Funky
        pass

    #Answer a yes-or-no question
    elif message.content.startswith('!ask'):
        await message.channel.send(fun.eightBall())

    #Convert a number to binary
    elif message.content.startswith('!binary'):
        await message.channel.send(useful.toBin(message))

    #List available commands
    elif message.content.startswith('!commands'):
        await message.channel.send(information.commandList())
        
    #Choose randomly from choices
    elif message.content.startswith('!choose'):
        await message.channel.send(fun.choose(message))

    #Say hello
    elif message.content.startswith('!hello'):
        await message.channel.send(information.sayHello(author, begin))

    #Send detailed instructions for commands
    elif message.content.startswith('!help'):
        await message.channel.send(information.sendHelp(message))

    #Convert a number to hexadecimal
    elif message.content.startswith('!hex'):
        await message.channel.send(useful.toHex(message))

    #Tell a joke
    elif message.content.startswith('!joke'):
        await message.channel.send(fun.findOneLiner())

    #Search for a Magic card
    elif message.content.startswith('!magic'):
        for c in useful.fetchCard(message):
            await message.channel.send(c)

    #Send a random reaction image
    elif message.content.startswith('!react'):
        try:
            await message.delete()
            helpers.logMessage(message)
        except discord.errors.Forbidden: #Can't delete
            pass
        try:
            await message.channel.send(file=discord.File(fun.reactionPic()))
        except RuntimeError: #If there are no valid images
            await message.channel.send("I didn't find any images!")

    #Rate something
    elif message.content.startswith('!rate'):
        await message.channel.send(fun.rateSomething(message))
                                       
    #Roll a die
    elif message.content.startswith('!roll'):
        await message.channel.send(useful.rollDice(message))                               

    #Send a shiba inu picture
    elif message.content.startswith('!shibe'):
        try:
            await message.channel.send(file=discord.File(fun.shibaPic()))
        except RuntimeError: #No valid images
            await message.channel.send("I didn't find any images!")

    #Setup a reminder
    elif message.content.startswith('!remind'):
        reminder = useful.makeReminder(message)

        await message.channel.send(useful.confirmReminder(message, reminder))

        def pred(msg):
            return (msg.author == message.author and
                    msg.channel == message.channel and
                    (msg.content.startswith('!yes') or msg.content.startswith('!no')))

        if reminder != None:
            try:
                reply = await client.wait_for('message', check=pred, timeout=10)
                if reply.content.startswith('!yes'):
                    await message.channel.send(useful.startReminder(reminder))
                elif reply.content.startswith('!no'):
                    await message.channel.send("Ok, I will discard that reminder.")
                    
            except asyncio.TimeoutError:      
                await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                          % message.author.mention)
                
    #Setup reminder for everyone
    elif message.content.startswith('!announce'):
        if(message.author.guild_permissions.administrator):
            reminder = useful.makeReminder(message)

            await message.channel.send(useful.confirmReminder(message, reminder))

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        (msg.content.startswith('!yes') or msg.content.startswith('!no')))

            try:
                reply = await client.wait_for('message', check=pred, timeout=10)
                if reply.content.startswith('!yes'):
                    await message.channel.send(useful.startReminder(reminder))
                elif reply.content.startswith('!no'):
                    await message.channel.send("Ok, I will discard that reminder.")
                    
            except asyncio.TimeoutError:
                await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                              % message.author.mention)
                
        else:
            await message.channel.send("Sorry, only administrators can use that command!")
        
#==== Log on ====
with open(helpers.filePath("token.txt"),'r') as o:
    token = o.readline()
    client.run(token)


