#==== Description ====
"""
Sends messages to Discord from information commands
"""

#==== Imports ====
from funktions import information, helpers
from errors import errors

#==== Say hello and give some information ====
async def hello(message,startTime):
    await message.channel.send(information.sayHello(message.author,startTime))

#==== Send list of commands or get instructions ====
async def help(message):
    try:
        await message.channel.send(information.sendHelp(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
