#==== Description ====
"""
Keeps track of reminder requests from users and sends reminders when ready
"""

#==== Imports ====
import asyncio
import re
from aiohttp import client_exceptions

from helpers.objects import timer
from helpers import (helper_functions as h,
                     global_vars as g)

#==== Reminder class ====
class Reminder():
    def __init__(self,duration=0,msg=None,dt=False):
        if msg != None:
            self.message = ""
            self._formatMessage(msg)
            self.destination = msg.channel.id

        self.duration = duration
        self.dt = dt
        
        self.begin = -1
        self.live = False
        self.id = -1
        self.timer = timer.Timer()

    def beginThread(self):
        if not self.live:
            self.live = True
            if self.begin < 0:
                if self.dt:
                    self.begin = 0
                else:
                    self.begin = h.getTime()
                    
            asyncio.ensure_future(self.__run())

    #Shouldn't be called outside of this class or subclasses
    def _formatMessage(self,cmd):
        message = re.sub("\[([^\[\]]*)\]", "",
                         cmd.content.split(' ',1)[1], flags=re.IGNORECASE)
        
        message = " ".join(message.split())
                
        self.message = "%s %s" % (cmd.author.mention,message)
        
    @asyncio.coroutine
    async def __run(self):
        await self.timer.timeUntilDate(self.duration + self.begin)
        
        while self.live:
            try:
                await g.client.get_channel(self.destination).send(self.message)
                self.live = False
                g.db.deleteReminder(self)
            #If bot is trying to reconnect, delay the message
            except client_exceptions.ClientConnectorError:
                await self.timer.timeForDuration(1)


#==== Announcement class ====
class Announcement(Reminder):
    def __init__(self,duration=0,msg=None,dt=False):
        super().__init__(duration=duration,msg=msg,dt=dt)

    def beginThread(self):
        super().beginThread()

    def _formatMessage(self,cmd):
        message = re.sub("\[([^\[\]]*)\]", "",
                         cmd.content.split(' ',1)[1], flags=re.IGNORECASE)
        message = " ".join(message.split())

        self.message = "@everyone" + " " + message
