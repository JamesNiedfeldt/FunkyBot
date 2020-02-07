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

#==== Globals ====
client = None
database = database.db

#==== Reminder class ====
class Reminder():
    def __init__(self,duration=0,msg=None):
        if(msg != None):
            self.message = ""
            self._formatMessage(msg)
            self.duration = duration
            self.begin = -1
            self.destination = msg.channel.id
        self.live = False
        self.id = -1

    def beginThread(self):
        if(self.begin == -1):
            self.begin = time.time()
        self.live = True
        asyncio.ensure_future(self.__run())

    #Shouldn't be called outside of this class or subclasses
    def _formatMessage(self,cmd):
        message = re.sub("(\[\[.*\]\])|(!remind)|(!announce)","",cmd.content)
        if message != "" and message[0] == " ":
            message = message[1:]
                
        self.message = "%s %s" % (cmd.author.mention,message)
        
    @asyncio.coroutine
    async def __run(self):
        while(self.live):
            if(time.time() >= self.begin + self.duration):
                self.live = False
                await client.send_message(client.get_channel(str(self.destination)),
                                          self.message)
                database.deleteFromDb(self)
                
            else:
                await asyncio.sleep(1)

#==== Announcement class ====
class Announcement(Reminder):
    def __init__(self,duration=0,msg=None):
        super().__init__(duration=duration,msg=msg)

    def beginThread(self):
        super().beginThread()

    def _formatMessage(self,cmd):
        message = re.sub("(\[\[.*\]\])|(!remind)|(!announce)","",cmd.content)
        if message != "" and message[0] == " ":
            message = message[1:]
             
        self.message = "@everyone" + " " + message
