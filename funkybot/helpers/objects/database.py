#==== Description ====
"""
Handles database work for FunkyBot reminders
"""

#==== Imports ====
import sqlite3
import time
import os

from helpers.objects import reminder

#==== Globals ====
db = None

#==== Database class ====
class Database():
    def __init__(self):
        self.db = None
        self.reminders = []
        self.dbConnect()

    #==== Connect to/create database ====
    def dbConnect(self):
        #TODO: make this less awful
        absolute = os.path.abspath(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__))))
        
        self.db = sqlite3.connect(os.path.join(absolute,"reminders.db"))
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
        (id INTEGER PRIMARY KEY,
        begin INTEGER,
        duration INTEGER,
        message STRING,
        destination STRING)''')

    #==== Register reminder in database ====
    def insertToDb(self,reminder):
        values = (reminder.begin, reminder.duration, reminder.message,
                  reminder.destination)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO reminders (begin, duration, message, destination)"+
                       "VALUES(?,?,?,?)",(values))
        reminder.id = cursor.lastrowid
        self.db.commit()
        
        if reminder.live:
            self.reminders.append(reminder)

    def deleteFromDb(self,reminder):
        if reminder.id != -1:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM reminders WHERE id=?",(reminder.id,))
            self.db.commit()

        try:
            self.reminders.remove(reminder)
        except ValueError:
            pass

    #==== Clear items from database ====
    def __emptyDb(self):
        self.db.execute("DELETE FROM reminders")
        self.db.commit()

    #==== Get reminders in database ====
    def __getFromDb(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reminders")
        for i in cursor.fetchall():
            newReminder = reminder.Reminder()
            
            #Add reminder only if an identical one isn't presently running
            if not any(r.id == i[0] for r in self.reminders):
                newReminder.id = i[0]
                newReminder.begin = i[1]
                newReminder.duration = i[2]
                newReminder.message = i[3]
                newReminder.destination = i[4]

                self.reminders.append(newReminder)

    #==== Create threads from reminders ====
    def runThreads(self):
        self.__getFromDb()
        for i in self.reminders:
            i.beginThread()

db = Database()
