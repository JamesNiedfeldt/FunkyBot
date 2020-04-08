#==== Description ====
"""
Keeps track of reminder requests from users and sends reminders when ready
"""

#==== Imports ====
import time
import asyncio
import re
import discord
from reminder import database
from aiohttp import client_exceptions

#==== Globals ====
client = None
database = database.db

#==== Reminder class ====
class Reminder():
    def __init__(self,duration=0,msg=None,dt=False):
        if(msg != None):
            self.message = ""
            self._formatMessage(msg)
            self.duration = duration
            self.begin = -1
            self.destination = msg.channel.id
        self.live = False
        self.id = -1
        self.dt = dt

    def beginThread(self):
        if not self.live:
            if self.begin == -1:
                if self.dt:
                    self.begin = 0
                else:
                    self.begin = time.time()
            self.live = True
            asyncio.ensure_future(self.__run())

    #Shouldn't be called outside of this class or subclasses
    def _formatMessage(self,cmd):
        message = re.sub("(\[\[.*\]\])|(!REMIND)|(!ANNOUNCE)", "",
                         cmd.content, flags=re.IGNORECASE)
        if message != "" and message[0] == " ":
            message = message[1:]
                
        self.message = "%s %s" % (cmd.author.mention,message)
        
    @asyncio.coroutine
    async def __run(self):
        while(self.live):
            if(time.time() >= self.begin + self.duration):
                try:
                    await client.get_channel(self.destination).send(self.message)
                    self.live = False
                    database.deleteFromDb(self)
                #If bot is trying to reconnect, delay the message
                except client_exceptions.ClientConnectorError:
                    await asyncio.sleep(1)
                
            else:
                await asyncio.sleep(1)

#==== Announcement class ====
class Announcement(Reminder):
    def __init__(self,duration=0,msg=None,dt=False):
        super().__init__(duration=duration,msg=msg,dt=dt)

    def beginThread(self):
        super().beginThread()

    def _formatMessage(self,cmd):
        message = re.sub("(\[\[.*\]\])|(!REMIND)|(!ANNOUNCE)", "",
                         cmd.content, flags=re.IGNORECASE)
        if message != "" and message[0] == " ":
            message = message[1:]
             
        self.message = "@everyone" + " " + message
