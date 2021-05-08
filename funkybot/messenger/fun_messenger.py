#==== Description ====
"""
Sends messages to Discord from fun commands
"""

#==== Imports ====
import discord

from funktions import fun
from helpers import helper_functions as helpers, global_vars as globs
from errors import errors

#==== Answer a yes or no question ====
async def ask(message):
    await message.channel.send(fun.eightBall())

#==== Choose between options ====
async def choose(message):
    try:
        await message.channel.send(fun.choose(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Send random cute animal image ====
async def cute(message, corrected):
    #If this command was sent via suggestion, don't delete
    if not corrected and globs.props['cute_delete'] == 'true':
        try:
            await message.delete()
            helpers.logMessage(message)
        except discord.errors.Forbidden: #Can't delete
            pass
    try:
        await message.channel.send(file=discord.File(fun.randomPic("cute_pics")))
    except (RuntimeError, FileNotFoundError): #No valid images or bad path
        await message.channel.send("I couldn't find any images!")

#==== Send a random joke ====
async def joke(message):
    await message.channel.send(fun.findOneLiner())

#==== Send random reaction image ====
async def react(message, corrected):
    #If this command was sent via suggestion, don't delete
    if not corrected and globs.props['react_delete'] == 'true': 
        try:
            await message.delete()
            helpers.logMessage(message)
        except discord.errors.Forbidden: #Can't delete
            pass
    try:
        await message.channel.send(file=discord.File(fun.randomPic("reaction_pics")))
    except (RuntimeError, FileNotFoundError): #No valid images or bad path
        await message.channel.send("I couldn't find any images!")

#==== Rate something ====
async def rate(message):
    try:
        await message.channel.send(fun.rateSomething(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
