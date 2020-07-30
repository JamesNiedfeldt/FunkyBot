import unittest
import os
from funktions_test import mockmessage as m
from funktions import information as i
from funktions import helpers as h
from funktions import constant as c

class TestInformation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_sayHello(self):
        sender = type("sender", (), {"display_name" : ""})
        uptime = h.getTime()

        sender.display_name = "Test Name"
        time = h.formatTime(0)
        msg = ((c.HELLO % sender.display_name) + "\n" +
            h.blockQuote("**Current version:** %s" % c.VERSION) +
            h.blockQuote("**Current uptime:** %s" % h.formatTime(h.getTime(),offset=uptime)))
        self.assertEqual(i.sayHello(sender, h.getTime()), msg)

        sender.display_name = ""
        time = h.formatTime(0)
        msg = ((c.HELLO % sender.display_name) + "\n" +
            h.blockQuote("**Current version:** %s" % c.VERSION) +
            h.blockQuote("**Current uptime:** %s" % h.formatTime(h.getTime(),offset=uptime)))
        self.assertEqual(i.sayHello(sender, h.getTime()), msg)
    
    def test_sendHelp(self):
        commands = ["hello", "help", "announce", "binary",
                    "hex", "magic", "remind", "roll", "ask", "choose",
                    "joke", "react", "rate", "shibe"]
        empty = ("Here are my commands:\n" +
                 h.blockQuote(c.INFO_LIST) +
                 h.blockQuote(c.USEFUL_LIST) +
                 h.blockQuote(c.FUN_LIST) + "\n" +
                 c.HELP_REMINDER)
        
        msg = m.MockMessage()

        msg.content = ""
        self.assertEqual(i.sendHelp(msg), empty)

        msg.content = "[[]]"
        self.assertEqual(i.sendHelp(msg), empty)

        msg.content = "[[x|y]]"
        expected = "I can only help you with one command at a time!"
        self.assertEqual(i.sendHelp(msg), expected)

        for o in commands:
            msg.content = "[[%s]]" % o
            self.assertIsNotNone(i.sendHelp(msg))
            msg.content = "[[!%s]]" % o
            self.assertIsNotNone(i.sendHelp(msg))
            msg.content = ("[[!%s]]" % o).upper()
            self.assertIsNotNone(i.sendHelp(msg))

        msg.content = "[[fake_command]]"
        expected = ("I don't have the command you're asking for." +
                    "\n\nIf you need a list of commands, send `!help` with no options.")
        self.assertEqual(i.sendHelp(msg), expected)

if __name__ == "__main__":
    unittest.main()
