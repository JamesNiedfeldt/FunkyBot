import unittest
import os
from funktions_test import mockmessage as m
from funktions import information as i
from helpers import helper_functions as h, constant as c
from errors import errors as err

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
                    "hex", "magic", "poll", "remind", "roll", "ask", "choose",
                    "joke", "react", "rate", "cute"]
        empty = ("Here are my commands:\n" +
                 h.blockQuote("**Information:** `!hello` `!help [[X]]`") +
                 h.blockQuote("**Useful:** `!announce [[X|...]]` `!binary [[X]]` `!hex [[X]]` `!magic [[X|...]]` `!poll [[X|Y|...]]` `!remind [[X|...]]` `!roll [[X]]` `!wiki [[X]]`") +
                 h.blockQuote("**Fun:** `!ask` `!choose [[X|Y|...]]` `!cute` `!joke` `!react` `!rate`") + "\n" +
                 c.HELP_REMINDER)
        
        msg = m.MockMessage()

        msg.content = ""
        self.assertEqual(i.sendHelp(msg), empty)

        msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, i.sendHelp, msg)

        msg.content = "[[x|y]]"
        self.assertRaises(err.TooManyArgumentsException, i.sendHelp, msg)

        for o in commands:
            msg.content = "[[%s]]" % o
            self.assertIsNotNone(i.sendHelp(msg))
            msg.content = "[[!%s]]" % o
            self.assertIsNotNone(i.sendHelp(msg))
            msg.content = ("[[!%s]]" % o).upper()
            self.assertIsNotNone(i.sendHelp(msg))

        msg.content = "[[fake_command]]"
        self.assertRaises(err.CustomCommandException, i.sendHelp, msg)

if __name__ == "__main__":
    unittest.main()
