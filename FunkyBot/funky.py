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
    elif message.content.upper().startswith('!ASK'):
        await message.channel.send(fun.eightBall())

    #Convert a number to binary
    elif message.content.upper().startswith('!BINARY'):
        await message.channel.send(useful.toBin(message))

    #List available commands
    elif message.content.upper().startswith('!COMMANDS'):
        await message.channel.send(information.commandList())
        
    #Choose randomly from choices
    elif message.content.upper().startswith('!CHOOSE'):
        await message.channel.send(fun.choose(message))

    #Say hello
    elif message.content.upper().startswith('!HELLO'):
        await message.channel.send(information.sayHello(author, begin))

    #Send detailed instructions for commands
    elif message.content.upper().startswith('!HELP'):
        await message.channel.send(information.sendHelp(message))

    #Convert a number to hexadecimal
    elif message.content.upper().startswith('!HEX'):
        await message.channel.send(useful.toHex(message))

    #Tell a joke
    elif message.content.upper().startswith('!JOKE'):
        await message.channel.send(fun.findOneLiner())

    #Search for a Magic card
    elif message.content.upper().startswith('!MAGIC'):
        for c in useful.fetchCard(message):
            if c[0] == None:
                await message.channel.send(c[1])
            else:
                await message.channel.send(c[0], embed=discord.Embed(title=c[1], description=c[2]).set_image(url=c[3]))

    #Send a random reaction image
    elif message.content.upper().startswith('!REACT'):
        try:
            await message.delete()
            helpers.logMessage(message)
        except discord.errors.Forbidden: #Can't delete
            pass
        try:
            await message.channel.send(file=discord.File(fun.randomPic("reaction_pics")))
        except (RuntimeError, FileNotFoundError): #If there are no valid images or bad path
            await message.channel.send("I didn't find any images!")

    #Rate something
    elif message.content.upper().startswith('!RATE'):
        await message.channel.send(fun.rateSomething(message))
                                       
    #Roll a die
    elif message.content.upper().startswith('!ROLL'):
        await message.channel.send(useful.rollDice(message))                               

    #Send a shiba inu picture
    elif message.content.upper().startswith('!SHIBE'):
        try:
            await message.channel.send(file=discord.File(fun.randomPic("shiba_pics")))
        except (RuntimeError, FileNotFoundError): #No valid images or bad path
            await message.channel.send("I didn't find any images!")

    #Setup a reminder
    elif message.content.upper().startswith('!REMIND'):
        reminder = useful.makeReminder(message)

        await message.channel.send(useful.confirmReminder(message, reminder))

        def pred(msg):
            return (msg.author == message.author and
                    msg.channel == message.channel and
                    (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

        if reminder != None:
            try:
                reply = await client.wait_for('message', check=pred, timeout=30)
                if reply.content.upper().startswith('!YES'):
                    await message.channel.send(useful.startReminder(reminder))
                elif reply.content.upper().startswith('!NO'):
                    await message.channel.send("Ok, I will discard that reminder.")
                    
            except asyncio.TimeoutError:      
                await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                          % message.author.mention)
                
    #Setup reminder for everyone
    elif message.content.upper().startswith('!ANNOUNCE'):
        if message.author.guild_permissions.administrator:
            reminder = useful.makeReminder(message, announcement=True)

            await message.channel.send(useful.confirmReminder(message, reminder))

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

            try:
                reply = await client.wait_for('message', check=pred, timeout=30)
                if reply.content.upper().startswith('!YES'):
                    await message.channel.send(useful.startReminder(reminder))
                elif reply.content.upper().startswith('!NO'):
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


