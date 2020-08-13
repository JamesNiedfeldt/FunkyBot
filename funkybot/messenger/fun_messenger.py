#==== Description ====
"""
Sends messages to Discord from fun commands
"""

#==== Imports ====
from funktions import fun, helpers
import discord

#==== Answer a yes or no question ====
async def ask(message):
    await message.channel.send(fun.eightBall())

#==== Choose between options ====
async def choose(message):
    await message.channel.send(fun.choose(message))

#==== Send random cute animal image ====
async def cute(message):
    try:
        await message.channel.send(file=discord.File(fun.randomPic("cute_pics")))
    except (RuntimeError, FileNotFoundError): #No valid images or bad path
        await message.channel.send("I couldn't find any images!")

#==== Send a random joke ====
async def joke(message):
    await message.channel.send(fun.findOneLiner())

#==== Send random reaction image ====
async def react(message):
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
    await message.channel.send(fun.rateSomething(message))
