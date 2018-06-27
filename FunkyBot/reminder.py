#==== Description ====
"""
Keeps track of reminder requests from users and sends reminders when ready
"""

#==== Imports ====
import re
import time
import sqlite3
import asyncio

db = None

#==== Connect to/create database ====
def dbConnect():
    db = sqlite3.connect("reminders.db")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
    (start INTEGER,
    duration INTEGER,
    message STRING)''')

#==== Clear items from database ====
def emptyDb():
    db.execute("DELETE FROM reminders")

#==== Get reminders in database ====
def getReminders():
    for i in db.execute("SELECT * FROM reminders"):
        reminders.append(i)

#==== Create threads from reminders ====
def runThreads():
    for i in reminders:
        i.start()

#==== Reminder class ====
class Reminder():
    def __init__(self,begin):
        self.message = ""
        self.duration = 0
        self.begin = begin
        self.live = False
        self.author = ""
        self.formattedMessage = ""
        self.channel = None
        self.func = None
        
        if(db == None):
            dbConnect()

    def setMessage(self,message):
        self.message = message

    def setDuration(self,duration):
        self.duration = duration

    def setAuthor(self,author):
        self.author = author

    def setChannel(self,channel):
        self.channel = channel

    def setFormattedMessage(self):
        self.formattedMessage = "%s %s" % (self.author.mention,self.message)

    def beginThread(self,func,loop):
        self.func = func
        self.live = True
        asyncio.ensure_future(self.run())

    @asyncio.coroutine
    async def run(self):
        print("started thread")
        self.begin = time.time()
        while(self.live):
            if(time.time() >= self.begin + self.duration):
                self.live = False
                await self.func
            else:
                await asyncio.sleep(1)
