#==== Description ====
"""
Keeps track of reminder requests from users and sends reminders when ready
"""

#==== Imports ====
import sqlite3
import time
import asyncio
import re
import discord
import os

#==== Globals ====
client = None
database = None

#==== Database class ====
class Database():
    def __init__(self):
        self.db = None
        self.reminders = []
        self.dbConnect()

    #==== Connect to/create database ====
    def dbConnect(self):
        absolute = os.path.abspath(os.path.dirname(__file__))
        self.db = sqlite3.connect(os.path.join(absolute,"reminders.db"))
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
        (id INTEGER PRIMARY KEY,
        begin INTEGER,
        duration INTEGER,
        message STRING,
        destination STRING,
        author STRING)''')

    #==== Register reminder in database ====
    def insertToDb(self,reminder):
        values = (reminder.begin, reminder.duration, reminder.message,
                  reminder.destination, reminder.author)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO reminders (begin, duration, message, destination, author)"+
                       "VALUES(?,?,?,?,?)",(values))
        reminder.id = cursor.lastrowid
        self.db.commit()

    def deleteFromDb(self,reminder):
        if(reminder.id != -1):
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM reminders WHERE id=?",(reminder.id,))
            self.db.commit()

    #==== Clear items from database ====
    def __emptyDb(self):
        self.db.execute("DELETE FROM reminders")
        self.db.commit()

    #==== Get reminders in database ====
    def __getFromDb(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reminders")
        for i in cursor.fetchall():
            reminder = Reminder()

            reminder.id = i[0]
            reminder.begin = i[1]
            reminder.duration = i[2]
            reminder.message = i[3]
            reminder.destination = i[4]
            reminder.author = i[5]

            self.reminders.append(reminder)

    #==== Create threads from reminders ====
    def runThreads(self):
        self.__getFromDb()
        for i in self.reminders:
            i.beginThread()
        print("Number of reminders from DB: %s" % len(self.reminders))

#==== Reminder class ====
class Reminder():
    def __init__(self,duration=0,msg=None):
        if(msg != None):
            self.message = re.sub("(\[\[.*\]\])|(!remind)","",msg.content)
            if(self.message[0] == " " and self.message != ""):
                self.message = self.message[1:]
            self.duration = duration
            self.begin = time.time()
            self.destination = msg.channel.id
            self.author = msg.author.mention
        self.live = False
        self.id = -1

    def beginThread(self):
        self.formattedMessage = "%s %s" % (self.author,self.message)
        self.live = True
        asyncio.ensure_future(self.__run())

    @asyncio.coroutine
    async def __run(self):
        while(self.live):
            if(time.time() >= self.begin + self.duration):
                self.live = False
                await client.send_message(client.get_channel(str(self.destination)),
                                          self.formattedMessage)
                database.deleteFromDb(self)
                
            else:
                await asyncio.sleep(1)

database = Database()
