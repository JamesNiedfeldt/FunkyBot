import unittest
import time
from funktions_test import mockmessage as m
from funktions import useful as u
from helpers import helper_functions as h
from helpers.objects import reminder as r
from errors import errors as err

class TestUseful(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = m.MockMessage()
        self.msg.author.mention = "test_mention"
        self.msg.channel.id = 100

        root = h.getXmlTree("userinfo")
        token = root.find("token").text
        self.apiheaders = {'User-Agent': root.find("user-agent").text,
              'From': root.find("email").text }

    def test_toBin(self):
        self.msg.content = "[[0]]"
        self.assertEqual(u.toBin(self.msg), "0 in binary is: 0")

        self.msg.content = "[[1]]"
        self.assertEqual(u.toBin(self.msg), "1 in binary is: 1")

        self.msg.content = "[[2]]"
        self.assertEqual(u.toBin(self.msg), "2 in binary is: 10")
        
        self.msg.content = "[[3]]"
        self.assertEqual(u.toBin(self.msg), "3 in binary is: 11")

        self.msg.content = "[[8]]"
        self.assertEqual(u.toBin(self.msg), "8 in binary is: 1000")

        self.msg.content = "[[16]]"
        self.assertEqual(u.toBin(self.msg), "16 in binary is: 10000")

        self.msg.content = "[[1023]]"
        self.assertEqual(u.toBin(self.msg), "1023 in binary is: 1111111111")

        self.msg.content = "[[65536]]"
        self.assertRaises(err.BadNumberException, u.toBin, self.msg)
        
        self.msg.content = "[[-1]]"
        self.assertRaises(err.BadNumberException, u.toBin, self.msg)

        self.msg.content = "[[1.25]]"
        self.assertRaises(err.BadValueException, u.toBin, self.msg)

        self.msg.content = "[[words]]"
        self.assertRaises(err.BadValueException, u.toBin, self.msg)

        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.toBin, self.msg)

        self.msg.content = "[[10|20]]"
        self.assertRaises(err.TooManyArgumentsException, u.toBin, self.msg)

    def test_toHex(self):
        self.msg.content = "[[0]]"
        self.assertEqual(u.toHex(self.msg), "0 in hexadecimal is: 0")

        self.msg.content = "[[1]]"
        self.assertEqual(u.toHex(self.msg), "1 in hexadecimal is: 1")

        self.msg.content = "[[10]]"
        self.assertEqual(u.toHex(self.msg), "10 in hexadecimal is: A")

        self.msg.content = "[[11]]"
        self.assertEqual(u.toHex(self.msg), "11 in hexadecimal is: B")

        self.msg.content = "[[12]]"
        self.assertEqual(u.toHex(self.msg), "12 in hexadecimal is: C")
        
        self.msg.content = "[[13]]"
        self.assertEqual(u.toHex(self.msg), "13 in hexadecimal is: D")

        self.msg.content = "[[14]]"
        self.assertEqual(u.toHex(self.msg), "14 in hexadecimal is: E")

        self.msg.content = "[[15]]"
        self.assertEqual(u.toHex(self.msg), "15 in hexadecimal is: F")

        self.msg.content = "[[16]]"
        self.assertEqual(u.toHex(self.msg), "16 in hexadecimal is: 10")

        self.msg.content = "[[256]]"
        self.assertEqual(u.toHex(self.msg), "256 in hexadecimal is: 100")

        self.msg.content = "[[4096]]"
        self.assertEqual(u.toHex(self.msg), "4096 in hexadecimal is: 1000")

        self.msg.content = "[[65535]]"
        self.assertEqual(u.toHex(self.msg), "65535 in hexadecimal is: FFFF")

        self.msg.content = "[[65536]]"
        self.assertRaises(err.BadNumberException, u.toHex, self.msg)

        self.msg.content = "[[-1]]"
        self.assertRaises(err.BadNumberException, u.toHex, self.msg)

        self.msg.content = "[[1.25]]"
        self.assertRaises(err.BadValueException, u.toHex, self.msg)

        self.msg.content = "[[words]]"
        self.assertRaises(err.BadValueException, u.toHex, self.msg)

        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.toHex, self.msg)

        self.msg.content = "[[10|20]]"
        self.assertRaises(err.TooManyArgumentsException, u.toHex, self.msg)

    @unittest.skip
    def test_fetchCard(self):
        #Each request must have a delay to comply with Scryfall's rate limits
        self.msg.content = "[[island|swamp|mountain|forest]]"
        self.assertRaises(err.TooManyArgumentsException, u.fetchCard, self.msg, self.apiheaders)

        time.sleep(.1)
        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.fetchCard, self.msg, self.apiheaders)

        time.sleep(.1)
        self.msg.content = "[[fake_card]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "Sorry, I couldn't find \"fake_card\"!")

        time.sleep(.1)
        self.msg.content = "[[random]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0].text)

        time.sleep(.1)
        self.msg.content = "[[random fake_card]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "Sorry, I couldn't find \"random fake_card\"!")

        time.sleep(.1)
        self.msg.content = "[[random c:rg]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0].text)

        time.sleep(.1)
        self.msg.content = "[[random c:rg|random is:commander]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 2)
        for card in results:
            self.assertIsNotNone(card)

        time.sleep(.1)
        self.msg.content = "[[plains]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0])
        self.assertNotIn("Sorry, I couldn't find", results[0].text)
        
        time.sleep(.1)
        self.msg.content = "[[plains|island]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 2)
        for card in results:
            self.assertIsNotNone(card.text)
            self.assertNotIn("Sorry, I couldn't find", card.text)

        time.sleep(.1)
        self.msg.content = "[[plains|island|swamp]]"
        results = u.fetchCard(self.msg, self.apiheaders)
        self.assertEqual(len(results), 3)
        for card in results:
            self.assertIsNotNone(card)
            self.assertNotIn("Sorry, I couldn't find", card.text)

    def test_makeReminder_noMessage(self):
        self.msg.content = " [[1s]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[30s]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1m]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1h]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1d]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1s|1h]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1m|1d]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1s|1m|1h]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000|20m]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[1s|1m|1h|1d]]"
        self.assertRaises(err.TooManyArgumentsException, u.makeReminder, self.msg)

        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.makeReminder, self.msg)

        self.msg.content = " [[31d]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[0]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[0s|0d|0h]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[-1d]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[-1d]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = "[[01/01/25 00:00 -0000]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = "[[01/01/1990 00:00 -0000]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = "[[20m|01/01/2025 00:00 -0000]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

    def test_makeReminder_withMessage(self):
        self.msg.content = "[[1s]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[30s]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m|1d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000|20m]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, self.msg.author.mention + " test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h|1d]] test message"
        self.assertRaises(err.TooManyArgumentsException, u.makeReminder, self.msg)

        self.msg.content = "[[]] test message"
        self.assertRaises(err.EmptyArgumentException, u.makeReminder, self.msg)

        self.msg.content = " [[31d]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[0]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[0s|0d|0h]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = " [[-1d]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = "[[01/01/1990 00:00 -0000]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

        self.msg.content = "[[20m|01/01/2025 00:00 -0000]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg)

    def test_makeReminder_announcmentNoMessage(self):
        self.msg.content = "[[1s]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[30s]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1h]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1d]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1h]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m|1d]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000|20m]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h|1d]]"
        self.assertRaises(err.TooManyArgumentsException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[31d]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[0]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[0s|0d|0h]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[-1d]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[01/01/1990 00:00 -0000]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[20m|01/01/2025 00:00 -0000]]"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

    def test_makeReminder_announcementWithMessage(self):
        self.msg.content = "[[1s]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[30s]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m|1d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[01/01/2025 00:00 -0000|20m]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1735689600)
        self.assertEqual(reminder.message, "@everyone test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h|1d]] test message"
        self.assertRaises(err.TooManyArgumentsException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[]] test message"
        self.assertRaises(err.EmptyArgumentException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[31d]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[0]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[0s|0d|0h]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = " [[-1d]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[01/01/1990 00:00 -0000]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

        self.msg.content = "[[20m|01/01/2025 00:00 -0000]] test message"
        self.assertRaises(err.CustomCommandException, u.makeReminder, self.msg, announcement=True)

    def test_confirmReminder(self):
        self.msg.content = " "
        
        reminder = r.Reminder(duration=30, msg=self.msg)
        expected = "Ok %s, I will remind you in %s. If that is ok, reply with `!yes`. If not, reply with `!no`." % (
            self.msg.author.display_name, h.formatTime(reminder.duration))
        self.assertEqual(u.confirmReminder(self.msg, reminder), expected)

        reminder = r.Announcement(duration=30, msg=self.msg)
        expected = "Ok %s, I will remind you in %s. If that is ok, reply with `!yes`. If not, reply with `!no`." % (
            self.msg.author.display_name, h.formatTime(reminder.duration))
        self.assertEqual(u.confirmReminder(self.msg, reminder), expected)

        self.assertEqual(u.confirmReminder(self.msg, ""), "")

    def test_startReminder(self):
        #TODO
        pass

    def test_rollDice(self):
        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.rollDice, self.msg)

        self.msg.content = "[[6|8]]"
        self.assertRaises(err.TooManyArgumentsException, u.rollDice, self.msg)

        self.msg.content = "[[0]]"
        self.assertRaises(err.BadNumberException, u.rollDice, self.msg)

        self.msg.content = "[[-1]]"
        self.assertRaises(err.BadNumberException, u.rollDice, self.msg)

        self.msg.content = "[[1001]]"
        self.assertRaises(err.BadNumberException, u.rollDice, self.msg)

        self.msg.content = "[[words]]"
        self.assertRaises(err.BadValueException, u.rollDice, self.msg)

        self.msg.content = "[[1.5]]"
        self.assertRaises(err.BadValueException, u.rollDice, self.msg)

        self.msg.content = "[[5]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[50]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[500]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[1000]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

    @unittest.skip
    def test_fetchWiki(self):
        #Each request must have a delay to comply with Wikipedia's rate limits
        self.msg.content = "[[]]"
        self.assertRaises(err.EmptyArgumentException, u.fetchWiki, self.msg, self.apiheaders)

        self.msg.content = "[[one|two]]"
        self.assertRaises(err.TooManyArgumentsException, u.fetchWiki, self.msg, self.apiheaders)

        time.sleep(.05)
        self.msg.content = "[[test fake article]]"
        results = u.fetchWiki(self.msg, self.apiheaders)
        self.assertEqual(results.text, "Sorry, I couldn't find \"test fake article\"!")

        time.sleep(.05)
        self.msg.content = "[[Wikipedia]]"
        results = u.fetchWiki(self.msg, self.apiheaders)
        self.assertIsNotNone(results.url)
        self.assertNotIn("Sorry, I couldn't find", results.text)

if __name__ == "__main__":
    unittest.main()
