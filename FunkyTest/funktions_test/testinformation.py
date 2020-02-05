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

    def test_commandList(self):
        self.assertIsNotNone(i.commandList())

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
        commands = ["commands", "hello", "help", "announce", "binary",
                    "hex", "magic", "remind", "roll", "ask", "choose",
                    "joke", "react", "rate", "shibe"]
        
        msg = m.MockMessage()

        msg.content = "[[]]"
        expected = h.badArgs("help") + "\n\nIf you need a list of commands, send `!commands`."
        self.assertEqual(i.sendHelp(msg), expected)

        msg.content = "[[x|y]]"
        expected = "I can only help you with one command at a time!"
        self.assertEqual(i.sendHelp(msg), expected)

        for c in commands:
            msg.content = "[[%s]]" % c
            self.assertIsNotNone(i.sendHelp(msg))
            msg.content = "[[!%s]]" % c
            self.assertIsNotNone(i.sendHelp(msg))

        msg.content = "[[fake_command]]"
        expected = h.badArgs("help") + "\n\nIf you need a list of commands, send `!commands`."
        self.assertEqual(i.sendHelp(msg), expected)

if __name__ == "__main__":
    unittest.main()
