#==== Description ====
"""
Sends messages to Discord from useful commands
"""

#==== Imports ====
from funktions import useful, helpers
import asyncio
import discord

#==== Setup a reminder for everyone ====
async def announce(message,client):
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

#==== Convert number to binary ====
async def binary(message):
    await message.channel.send(useful.toBin(message))

#==== Convert number to hexadecimal ====
async def hexadec(message):
    await message.channel.send(useful.toHex(message))

#==== Search for Magic cards ====
async def magic(message,apiHeaders):
    for c in useful.fetchCard(message,apiHeaders):
        if c[0] == None:
            await message.channel.send(c[1])
        else:
            await message.channel.send(c[0], embed=discord.Embed(title=c[1], description=c[2]).set_image(url=c[3]))

#==== Setup a poll ====
async def poll(message,client):
    activeId = str(message.author.id) + str(message.channel.id)

    if helpers.isPollRunning(activeId): #Only begin a poll if not already one in channel
        await message.channel.send("Sorry, you already have a poll running in this channel. If you want to end it, send `!end`.")

    else:
        poll = useful.makePoll(message)
        reactions = []
                                   
        if isinstance(poll, str): #Something went wrong, so an error was returned 
            await message.channel.send(poll)
            
        else:
            helpers.addToActivePolls(activeId)
            sentMsg = await message.channel.send(poll.body)

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        msg.content.upper().startswith('!END'))

            for o in poll.options:
                await sentMsg.add_reaction(o)

            try:
                reply = await client.wait_for('message', check=pred, timeout = 3600)
            except asyncio.TimeoutError:
                pass

            fetchedMsg = await message.channel.fetch_message(sentMsg.id) #Update message information
            await message.channel.send(useful.finishPoll(fetchedMsg,poll))
            helpers.removeFromActivePolls(activeId)

#==== Setup reminder ====
async def remind(message,client):
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

#==== Roll a die ====
async def roll(message):
    await message.channel.send(useful.rollDice(message))

#==== Search for a Wikipedia article ====
async def wiki(message,apiHeaders):
    a = useful.fetchWiki(message,apiHeaders)
    if a[0] == None:
        await message.channel.send(a[1])
    else:
        await message.channel.send(a[0], embed=discord.Embed(title=a[1], description=a[2]).set_image(url=a[3]))
