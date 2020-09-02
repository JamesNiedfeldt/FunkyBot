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
        self.msg.guild = "test server"
        self.msg.created_at = datetime.datetime(2000,1,1)
        self.msg.channel = "test channel"
        self.msg.author.name = "test author"
        self.msg.content = "test content"

        self.logpath = os.path.abspath(
            os.path.join(os.pardir, "funkybot/files/logs/%s-log.txt" % self.msg.guild))

    def test_parse(self):
        string = "[[]]"
        self.assertEqual(h.parse(string), [])

        string = "[[x|]]"
        self.assertEqual(h.parse(string), [])

        string = "[[|x]]"
        self.assertEqual(h.parse(string), [])

        string = "[]]"
        self.assertIsNone(h.parse(string))

        string = "[]"
        self.assertIsNone(h.parse(string))

        string = ""
        self.assertIsNone(h.parse(string))

        string = "[[x]]"
        self.assertEqual(h.parse(string), ['x'])

        string = "[[x|y]]"
        self.assertEqual(h.parse(string), ['x', 'y'])

    def test_logMessage(self):
        h.logMessage(self.msg)
        string = "%s - %s - %s: %s\n" % (
            self.msg.created_at.strftime("%Y-%b-%d %H:%M"), self.msg.channel,
            self.msg.author.name, self.msg.content)
        with open(self.logpath) as f:
            self.assertEqual(f.readline(), string)

    def test_validFolder(self):
        files = [1, 2]
        self.assertTrue(h.validFolder(files))

        files = [1]
        self.assertFalse(h.validFolder(files))

        files = []
        self.assertFalse(h.validFolder(files))

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
        abspath = head[0] + "/funkybot"
        
        path = os.path.join(abspath, "files/test_directory")
        self.assertEqual(h.filePath("test_directory"), path)

        path = os.path.join(abspath, "files/")
        self.assertEqual(h.filePath(""), path)

    def test_badArgs(self):
        msg = "I couldn't understand your command!\n\nIf you need more help with this command, send `!help [[!help]]`."
        self.assertEqual(h.badArgs("help"), msg)
        
        msg = ("I couldn't understand your command!\n\n"
               + "Make sure the command you want help with is surrounded by double brackets. "
               + "If you want a list of all commands, don't send any brackets. "
               + "If you need more help with this command, send `!help [[!help]]`.")
        self.assertEqual(h.badArgs("help", "brackets"), msg)

        msg = ("I couldn't understand your command!\n\n"
               + "I need a command to search for. "
               + "If you want a list of all commands, don't send any brackets. "
               + "If you need more help with this command, send `!help [[!help]]`.")
        self.assertEqual(h.badArgs("help", "too_few"), msg)

        msg = ("I couldn't understand your command!\n\n"
               + "I can only search for one command at a time. "
               + "If you need more help with this command, send `!help [[!help]]`.")
        self.assertEqual(h.badArgs("help", "too_many"), msg)

        msg = ("I couldn't understand your command!\n\n"
               + "I don't have the command you're searching for. "
               + "If you want a list of all commands, send `!help` with no arguments. "
               + "If you need more help with this command, send `!help [[!help]]`.")
        self.assertEqual(h.badArgs("help", "bad_command"), msg)

        msg = "I couldn't understand your command!\n\nIf you need more help with this command, send `!help [[!]]`."
        self.assertEqual(h.badArgs(""), msg)

    def test_blockQuote(self):
        msg = "> test\n"
        self.assertEqual(h.blockQuote("test"), msg)

        msg = "> \n"
        self.assertEqual(h.blockQuote(""), msg)

    def test_setUpReminders(self):
        #Nothing to test
        pass

    def test_convertDurationTime(self):
        args = ['1s']
        self.assertEqual(h.convertDurationTime(args), 1)

        args = ['1m']
        self.assertEqual(h.convertDurationTime(args), 60)

        args = ['1h']
        self.assertEqual(h.convertDurationTime(args), 3600)

        args = ['1d']
        self.assertEqual(h.convertDurationTime(args), 86400)

        args = ['5m']
        self.assertEqual(h.convertDurationTime(args), 300)

        args = ['1m', '30s']
        self.assertEqual(h.convertDurationTime(args), 90)

        args = ['5s', '2m', '1h']
        self.assertEqual(h.convertDurationTime(args), 3725)

        args = ['5s', '2m', '1h', '6d']
        self.assertEqual(h.convertDurationTime(args), 3725)

        args = ['5q']
        self.assertIsNone(h.convertDurationTime(args))

        args = ['1m', '5q']
        self.assertIsNone(h.convertDurationTime(args))

        args = []
        self.assertEqual(h.convertDurationTime(args), 0)

    def test_convertDateTime(self):
        args = ['01/01/2025 00:00 -0000']
        self.assertEqual(h.convertDateTime(args), 1735689600)

        args = ['01/01/2025 00:00 -0000', '']
        self.assertEqual(h.convertDateTime(args), 1735689600)

        args = ['01/01/1990 00:00 -0000']
        self.assertEqual(h.convertDateTime(args), -1)

        args = ['', '01/01/2025 00:00 -0000']
        self.assertIsNone(h.convertDateTime(args))

        args = ['01/01/25 00:00 -0000']
        self.assertIsNone(h.convertDateTime(args))

    def test_isPollRunning(self):
        #Nothing to test
        pass

    def test_removeFromActivePolls(self):
        #Nothing to test
        pass

    def test_getXmlTree(self):
        self.assertIsNotNone(h.getXmlTree("commands"))
    
    def tearDown(self):
        if(os.path.isfile(self.logpath)):
            os.remove(self.logpath)
        

if __name__ == "__main__":
    unittest.main()
    
