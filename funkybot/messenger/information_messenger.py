#==== Description ====
"""
Sends messages to Discord from information commands
"""

#==== Imports ====
import discord

from funktions import information
from helpers import helper_functions as helpers, constant
from errors import errors

#==== Say hello and give some information ====
async def hello(message,startTime,client):
    e = information.sayHello(startTime)
    av = client.user.avatar_url
    if av is None:
        av = ""
    emb = discord.Embed(title=e.title, description=e.text, url=e.url)
    emb.set_thumbnail(url=av).set_footer(text=e.footer)

    await message.channel.send(constant.HELLO % message.author.display_name,
                               embed=emb)

#==== Send list of commands or get instructions ====
async def help(message):
    try:
        await message.channel.send(information.sendHelp(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Correct user if an incorrect command was sent
async def unknown(message):
    cmd = helpers.parseUnknown(message.content)
    if cmd != None:
        await message.channel.send(cmd)
