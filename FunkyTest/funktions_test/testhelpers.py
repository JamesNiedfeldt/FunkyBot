import unittest
import discord
import datetime
import os
from funktions_test import mockmessage as m
from funktions import helpers as h
from reminder import database as db
from reminder import reminder as r

class TestHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = m.MockMessage()
        self.msg.server = "test server"
        self.msg.timestamp = datetime.datetime(2000,1,1)
        self.msg.channel = "test channel"
        self.msg.author.name = "test author"
        self.msg.content = "test content"

        self.logpath = os.path.abspath(
            os.path.join(os.pardir, "FunkyBot/logs/%s-log.txt" % self.msg.server))

    def test_parse(self):
        string = "[[]]"
        self.assertEqual(h.parse(string), [])

        string = "[[x|]]"
        self.assertEqual(h.parse(string), [])

        string = "[[|x]]"
        self.assertEqual(h.parse(string), [])

        string = ""
        self.assertEqual(h.parse(string), [])

        string = "[[x]]"
        self.assertEqual(h.parse(string), ['x'])

        string = "[[x|y]]"
        self.assertEqual(h.parse(string), ['x', 'y'])

    def test_logMessage(self):
        h.logMessage(self.msg)
        string = "%s - %s - %s: %s\n" % (
            self.msg.timestamp.strftime("%Y-%b-%d %H:%M"), self.msg.channel,
            self.msg.author.name, self.msg.content)
        with open(self.logpath) as f:
            self.assertEqual(f.readline(), string)

    def test_validFolder(self):
        files = [1, 2]
        try:
            h.validFolder(files)
        except RuntimeError:
            self.fail()

        files = [1]
        with self.assertRaises(RuntimeError):
            h.validFolder(files)

        files = []
        with self.assertRaises(RuntimeError):
            h.validFolder(files)

    def test_getTime(self):
        #Nothing to test
        pass

    def test_formatTime(self):
        string = "0 days, 0 hours, 0 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(0), string)
        
        string = "0 days, 0 hours, 0 minutes, and 30 seconds"
        self.assertEqual(h.formatTime(30), string)

        string = "0 days, 0 hours, 1 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(60), string)

        string = "0 days, 1 hours, 0 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(3600), string)

        string = "1 days, 0 hours, 0 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(86400), string)

        string = "2 days, 2 hours, 2 minutes, and 2 seconds"
        self.assertEqual(h.formatTime(180122), string)

        string = "0 days, 0 hours, 0 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(30, 30), string)

        string = "0 days, 0 hours, 0 minutes, and 30 seconds"
        self.assertEqual(h.formatTime(60, 30), string)

        string = "0 days, 0 hours, 1 minutes, and 0 seconds"
        self.assertEqual(h.formatTime(90, 30), string)

        string = "Error: Invalid time"
        self.assertEqual(h.formatTime(30, 31), string)

        string = "Error: Invalid time"
        self.assertEqual(h.formatTime(-30), string)

    def test_filePath(self):
        head = os.path.split(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        abspath = head[0] + "/FunkyBot"
        
        path = os.path.join(abspath, "test_directory")
        self.assertEqual(h.filePath("test_directory"), path)

        path = os.path.join(abspath, "")
        self.assertEqual(h.filePath(""), path)

    def test_badArgs(self):
        msg = "I couldn't understand your command! If you need help, send `!help [[!test]]`."
        self.assertEqual(h.badArgs("test"), msg)

        msg = "I couldn't understand your command! If you need help, send `!help [[!]]`."
        self.assertEqual(h.badArgs(""), msg)

    def test_setUpReminders(self):
        #Nothing to test
        pass
    
    def tearDown(self):
        if(os.path.isfile(self.logpath)):
            os.remove(self.logpath)
        

if __name__ == "__main__":
    unittest.main()
    
