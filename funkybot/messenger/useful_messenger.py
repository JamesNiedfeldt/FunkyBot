#==== Description ====
"""
Sends messages to Discord from useful commands
"""

#==== Imports ====
import asyncio
import discord

from funktions import useful
from helpers import helper_functions as helpers, global_vars as globs, constant as c
from errors import errors

#==== Setup a reminder for everyone ====
async def announce(message):
    if message.author.guild_permissions.administrator:
        try:
            reminder = useful.makeDateReminder(message, announcement=True)

            await message.channel.send(useful.confirmReminder(message, reminder))

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

            try:
                reply = await globs.client.wait_for('message', check=pred, timeout=30)
                if reply.content.upper().startswith('!YES'):
                    await message.channel.send(useful.startReminder(reminder))
                elif reply.content.upper().startswith('!NO'):
                    await message.channel.send("Ok, I will discard that reminder.")
                    
            except asyncio.TimeoutError:
                await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                              % message.author.mention)
        except errors.Error as e:
            await message.channel.send(helpers.badArgs(e))
            
    else:
        await message.channel.send("Sorry, only administrators can use that command!")

#==== Convert number to binary ====
async def binary(message):
    try:
        await message.channel.send(useful.toBin(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Calculate an equation ====
async def calc(message):
    try:
        await message.channel.send(useful.calc(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Convert number to hexadecimal ====
async def hexadec(message):
    try:
        await message.channel.send(useful.toHex(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Search for a Wikipedia article ====
async def game(message):
    try:
        a = useful.fetchGame(message)
        if a.empty():
            await message.channel.send(a.description)
        else:
            await message.channel.send("", embed=discord.Embed.from_dict(a.asDict()))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Search for Magic cards ====
async def magic(message):
    try:
        for c in useful.fetchCard(message):
            if c.empty():
                await message.channel.send(c.description)
            else:
                await message.channel.send("", embed=discord.Embed.from_dict(c.asDict()))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
            
#==== Setup a poll ====
async def poll(message):
    try:
        poll = useful.makePoll(message)
        
        if helpers.isPollRunning(poll): #Only begin a poll if not already one in channel
            await message.channel.send(c.POLL_ALREADY_RUNNING)
        elif message.guild.me.permissions_in(message.channel).add_reactions == False:
            await message.channel.send(c.CANT_ADD_REACTIONS)

        else:
            reactions = []
            sentMsg = await message.channel.send(poll.body)
            poll.messageId = sentMsg.id
            helpers.addToActivePolls(poll)

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        msg.content.upper().startswith('!END'))

            if globs.props['poll_pin']:
                try:
                    await sentMsg.pin(
                        reason="Poll started by %s: '%s'" % (poll.author, poll.question))
                except discord.errors.Forbidden: #Can't pin
                    pass

            for o in poll.options:
                await sentMsg.add_reaction(o)

            try:
                reply = await globs.client.wait_for(
                    'message', check=pred, timeout = int(globs.props['poll_run_duration']) * 3600)
            except asyncio.TimeoutError:
                pass

            fetchedMsg = await message.channel.fetch_message(poll.messageId) #Update message information
            await message.channel.send(useful.finishPoll(fetchedMsg,poll))

            try:
                await fetchedMsg.unpin(
                    reason="Poll by %s finished: '%s'" % (poll.author, poll.question))
            except discord.errors.Forbidden: #Can't unpin
                pass
            
            helpers.removeFromActivePolls(poll)
            
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Setup reminder ====
async def remind(message, time=False):
    try:
        if time:
            reminder = useful.makeDurationReminder(message)
        else:
            reminder = useful.makeDateReminder(message)

        await message.channel.send(useful.confirmReminder(message, reminder))

        def pred(msg):
            return (msg.author == message.author and
                    msg.channel == message.channel and
                    (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

        try:
            reply = await globs.client.wait_for('message', check=pred, timeout=30)
            if reply.content.upper().startswith('!YES'):
                await message.channel.send(useful.startReminder(reminder))
            elif reply.content.upper().startswith('!NO'):
                await message.channel.send("Ok, I will discard that reminder.")
                
        except asyncio.TimeoutError:      
            await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                      % message.author.mention)

    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Roll a die ====
async def roll(message):
    try:
        await message.channel.send(useful.rollDice(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Search for a Wikipedia article ====
async def wiki(message):
    try:
        a = useful.fetchWiki(message)
        if a.empty():
            await message.channel.send(a.description)
        else:
            await message.channel.send("", embed=discord.Embed.from_dict(a.asDict()))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
