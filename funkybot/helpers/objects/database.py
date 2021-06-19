#==== Description ====
"""
Handles database work for FunkyBot reminders
"""

#==== Imports ====
import sqlite3
import time
import os

from helpers import global_vars as g
from helpers.objects import reminder

#==== Database class ====
class Database():
    def __init__(self):
        self.db = None
        self.dbConnect()

    #==== Connect to/create database ====
    def dbConnect(self):
        absolute = os.path.abspath(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__))))
        
        self.db = sqlite3.connect(os.path.join(absolute,"funkydata.db"))
        self.__createRemindersTable()
        self.__createCommandUsageTable()

    #==== Create tables ====
    def __createRemindersTable(self):
        query = ("CREATE TABLE IF NOT EXISTS reminders\n" +
                 "(id INTEGER PRIMARY KEY,\n" +
                 "begin INTEGER,\n" +
                 "duration INTEGER,\n" +
                 "message STRING,\n" +
                 "destination STRING)")
        self.db.cursor().execute(query)
        self.db.commit()

    def __createCommandUsageTable(self):
        query = ("CREATE TABLE IF NOT EXISTS command_usage\n" +
                 "(id INTEGER PRIMARY KEY,\n" +
                 "name STRING,\n" +
                 "count INTEGER)")
        self.db.cursor().execute(query)
        self.db.commit()

    #==== Reminder functions ====
    def insertReminder(self,reminder):
        if self.db != None:
            values = (reminder.begin, reminder.duration, reminder.message,
                      reminder.destination)
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO reminders (begin, duration, message, destination)"+
                           "VALUES(?,?,?,?)",(values))
            reminder.id = cursor.lastrowid
            self.db.commit()
            
            if reminder.live:
                g.reminders.append(reminder)
        else:
            raise RuntimeError("Database was not initialized")

    def deleteReminder(self,reminder):
        if self.db != None:
            if reminder.id != -1:
                self.db.cursor().execute("DELETE FROM reminders WHERE id=?",(reminder.id,))
                self.db.commit()

            try:
                g.reminders.remove(reminder)
            except ValueError:
                pass
        else:
            raise RuntimeError("Database was not initialized")
        
    def loadReminders(self):
        if self.db != None:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM reminders")
            self.db.commit()

            for i in cursor.fetchall():
                newReminder = reminder.Reminder()
        
                #Add reminder only if an identical one isn't presently running
                if not any(r.id == i[0] for r in g.reminders):
                    newReminder.id = i[0]
                    newReminder.begin = i[1]
                    newReminder.duration = i[2]
                    newReminder.message = i[3]
                    newReminder.destination = i[4]

                    g.reminders.append(newReminder)
        else:
            raise RuntimeError("Database was not initialized")

    #==== Command usage functions ====
    def incrementCommand(self, cmd):
        if self.db != None:
            queryUpdate = ("UPDATE command_usage SET count=count+1\n" +
                           "WHERE name=?")
            queryInsert = ("INSERT INTO command_usage(name,count)\n" +
                           "SELECT ?, 1\n" +
                           "WHERE (SELECT Changes()=0)")
            self.db.execute(queryUpdate, (cmd,))
            self.db.execute(queryInsert, (cmd,))
            self.db.commit()
        else:
            raise RuntimeError("Database was not initialized")

    def getTopCommands(self):
        if self.db != None:
            query = ("SELECT name, count FROM command_usage "+
                     "ORDER BY count DESC LIMIT 5 ")
            lst = [list(i) for i in self.db.execute(query).fetchall()]
            self.db.commit()

            return lst
        else:
            raise RuntimeError("Database was not initialized")

    def clearCommands(self):
    #ONLY use if the reset_command_usage property is set to true!
        if self.db != None:
            self.db.execute("DELETE FROM command_usage")
            self.db.commit()
