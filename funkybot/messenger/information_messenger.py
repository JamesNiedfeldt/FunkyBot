#==== Description ====
"""
Sends messages to Discord from information commands
"""

#==== Imports ====
import discord

from funktions import information
from helpers import (helper_functions as helpers,
                     constant,
                     global_vars as globs)
from errors import errors

#==== Say hello and give some information ====
async def hello(message):
    e = information.sayHello()

    await message.channel.send(constant.HELLO % message.author.display_name,
                               embed=discord.Embed.from_dict(e.asDict()))

#==== Send list of commands or get instructions ====
async def help(message):
    try:
        m = information.sendHelp(message)
        if m.empty():
            await message.channel.send(m.description)
        else:
            await message.channel.send("Here are my commands:",
                                       embed=discord.Embed.from_dict(m.asDict()))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
