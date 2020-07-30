#==== Description ====
"""
Sends messages to Discord from information commands
"""

#==== Imports ====
from funktions import information

#==== Say hello and give some information ====
async def hello(message,startTime):
    await message.channel.send(information.sayHello(message.author,startTime))

#==== Send list of commands or get instructions ====
async def help(message):
    await message.channel.send(information.sendHelp(message))
