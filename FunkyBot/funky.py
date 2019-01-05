#==== Imports ====
import discord
import asyncio
import funktions

#==== Definitions ====
client = discord.Client()
version = "1.3.2"
with open(funktions.filePath("lists/blacklist.txt"), 'r') as o: #Load blacklist
    #Updating the blacklist requires restarting FunkyBot
    blacklist = o.readlines()
begin = funktions.upTime() #Time when Funky begins running

#==== Alert that Funky is ready ====
@client.event
async def on_ready():
    print("===============")
    print(client.user.name+" "+version)
    print("I'm ready to work!\n")
    funktions.setUpReminders(client)

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
        await client.send_message(message.channel, funktions.eightBall())

    #Convert a number to binary
    elif message.content.startswith('!binary'):
        await client.send_message(message.channel, funktions.toBin(message))

    #List available commands
    elif message.content.startswith('!commands'):
        await client.send_message(message.channel, funktions.commandList())

    #Choose randomly from choices
    elif message.content.startswith('!choose'):
        await client.send_message(message.channel, funktions.choose(message))

    #Say hello
    elif message.content.startswith('!hello'):
        await client.send_message(message.channel, funktions.sayHello(author,version,begin))

    #Send detailed instructions for commands
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, funktions.sendHelp(message))

    #Convert a number to hexadecimal
    elif message.content.startswith('!hex'):
        await client.send_message(message.channel, funktions.toHex(message))

    #Tell a joke
    elif message.content.startswith('!joke'):
        await client.send_message(message.channel, funktions.findOneLiner())

    #Search for a Magic card
    elif message.content.startswith('!magic'):
        for c in set(funktions.fetchCard(message)):
            await client.send_message(message.channel, c)

    #Send a random reaction image
    elif message.content.startswith('!react'):
        try:
            await client.delete_message(message)
            funktions.logMessage(message)
        except discord.errors.Forbidden: #Can't delete
            pass
        try:
            await client.send_file(message.channel, funktions.reactionPic())
        except RuntimeError: #If there are no valid images
            await client.send_message(message.channel, "I didn't find any images!")

    #Rate something
    elif message.content.startswith('!rate'):
        await client.send_message(message.channel, funktions.rateSomething(message))

    #Roll a die
    elif message.content.startswith('!roll'):
        await client.send_message(message.channel, funktions.rollDice(message))

    #Send a shiba inu picture
    elif message.content.startswith('!shibe'):
        try:
            await client.send_file(message.channel, funktions.shibaPic())
        except RuntimeError: #No valid images
            await client.send_message(message.channel, "I didn't find any images!")

    #Setup a reminder
    elif message.content.startswith('!remind'):
        reminder = funktions.makeReminder(message)
        
        await client.send_message(message.channel, funktions.confirmReminder(message,reminder))

        def check(msg):
            return msg.content.startswith('!yes') or msg.content.startswith('!no')

        if(reminder != None):
            reply = await client.wait_for_message(author=message. author,channel=message.channel,
                                                  timeout=60, check=check)
            
            if(reply == None):
                await client.send_message(message.channel, "%s, you took too long to respond so I discarded your reminder."
                                          % message.author.mention)
            elif(reply.content.startswith('!yes')):
                await client.send_message(message.channel, funktions.startReminder(reminder))
            elif(reply.content.startswith('!no')):
                await client.send_message(message.channel, "Ok, I will discard that reminder.")
        
        
#==== Log on ====
with open(funktions.filePath("token.txt"),'r') as o:
    token = o.readline()
    client.run(token)
    o.close()


