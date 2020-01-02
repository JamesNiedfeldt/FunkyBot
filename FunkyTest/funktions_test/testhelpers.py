import unittest
import discord
import datetime
import os
from funktions_test import mockmessage as m
from funktions import helpers as h

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

    

    def tearDown(self):
        if(os.path.isfile(self.logpath)):
            os.remove(self.logpath)
        

if __name__ == "__main__":
    unittest.main()
    
