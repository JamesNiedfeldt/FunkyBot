import unittest
import time
from funktions_test import mockmessage as m
from funktions import helpers as h
from funktions import useful as u
from reminder import reminder as r

class TestUseful(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = m.MockMessage()
        self.msg.author.mention = "test_mention"
        self.msg.channel.id = 100

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

        self.msg.content = "[[1024]]"
        self.assertEqual(u.toBin(self.msg), "Sorry, I can't convert 1024 to binary!")

        self.msg.content = "[[-1]]"
        self.assertEqual(u.toBin(self.msg), "Sorry, I can't convert -1 to binary!")

        self.msg.content = "[[1.25]]"
        self.assertEqual(u.toBin(self.msg), "Sorry, I can't convert 1.25 to binary!")

        self.msg.content = "[[words]]"
        self.assertEqual(u.toBin(self.msg), "Sorry, I can't convert words to binary!")

        self.msg.content = "[[]]"
        self.assertEqual(u.toBin(self.msg), h.badArgs("binary"))

        self.msg.content = "[[10|20]]"
        self.assertEqual(u.toBin(self.msg), "I can only convert one number!")

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
        self.assertEqual(u.toHex(self.msg), "Sorry, I can't convert 65536 to hexadecimal!")

        self.msg.content = "[[-1]]"
        self.assertEqual(u.toHex(self.msg), "Sorry, I can't convert -1 to hexadecimal!")

        self.msg.content = "[[1.25]]"
        self.assertEqual(u.toHex(self.msg), "Sorry, I can't convert 1.25 to hexadecimal!")

        self.msg.content = "[[words]]"
        self.assertEqual(u.toHex(self.msg), "Sorry, I can't convert words to hexadecimal!")

        self.msg.content = "[[]]"
        self.assertEqual(u.toHex(self.msg), h.badArgs("hex"))

        self.msg.content = "[[10|20]]"
        self.assertEqual(u.toHex(self.msg), "I can only convert one number!")

    def test_fetchCard(self):
        #Each request must have a delay to comply with Scryfall's rate limits
        self.msg.content = "[[island|swamp|mountain|forest]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "That's too many cards to search for!")

        time.sleep(.1)
        self.msg.content = "[[]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], h.badArgs("magic"))

        time.sleep(.1)
        self.msg.content = "[[fake_card]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "Sorry, I couldn't find \"fake_card\"!")

        time.sleep(.1)
        self.msg.content = "[[random]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0], "Sorry, I couldn't find \"fake_card\"!")

        time.sleep(.1)
        self.msg.content = "[[plains]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 1)
        self.assertNotIn("Sorry, I couldn't find", results[0])
        
        time.sleep(.1)
        self.msg.content = "[[plains|island]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 2)
        for string in results:
            self.assertNotIn("Sorry, I couldn't find", string)

        time.sleep(.1)
        self.msg.content = "[[plains|island|swamp]]"
        results = u.fetchCard(self.msg)
        self.assertEqual(len(results), 3)
        for string in results:
            self.assertNotIn("Sorry, I couldn't find", string)

    def test_makeReminder_noMessage(self):
        self.msg.content = "[[]]"
        self.assertIsNone(u.makeReminder(self.msg))

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

        self.msg.content = " [[1s|1m|1h|1d]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[31d]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 2592000)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[0]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = " [[0s|0d|0h]]"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, self.msg.author.mention + " ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

    def test_makeReminder_withMessage(self):
        self.msg.content = "[[]] test message"
        self.assertIsNone(u.makeReminder(self.msg))

        self.msg.content = "[[1s]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[30s]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m|1d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h|1d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[31d]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 2592000)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0s|0d|0h]] test message"
        reminder = u.makeReminder(self.msg)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, self.msg.author.mention + "  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

    def test_makeReminder_announcmentNoMessage(self):
        self.msg.content = "[[]]"
        self.assertIsNone(u.makeReminder(self.msg, announcement=True))

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

        self.msg.content = "[[1s|1m|1h|1d]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[31d]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 2592000)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0s|0d|0h]]"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, "@everyone ")
        self.assertEqual(reminder.destination, self.msg.channel.id)

    def test_makeReminder_announcementWithMessage(self):
        self.msg.content = "[[]] test message"
        self.assertIsNone(u.makeReminder(self.msg, announcement=True))

        self.msg.content = "[[1s]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 1)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[30s]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 30)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 60)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3600)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86400)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3601)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1m|1d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 86460)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[1s|1m|1h|1d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 3661)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[31d]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 2592000)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

        self.msg.content = "[[0s|0d|0h]] test message"
        reminder = u.makeReminder(self.msg, announcement=True)
        self.assertEqual(reminder.duration, 300)
        self.assertEqual(reminder.message, "@everyone  test message")
        self.assertEqual(reminder.destination, self.msg.channel.id)

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

        self.assertEqual(u.confirmReminder(self.msg, None), h.badArgs("remind"))

    def test_startReminder(self):
        #TODO
        pass

    def test_rollDice(self):
        self.msg.content = "[[]]"
        self.assertEqual(u.rollDice(self.msg), h.badArgs("roll"))

        self.msg.content = "[[6|8]]"
        self.assertEqual(u.rollDice(self.msg), "I can only roll one die!")

        self.msg.content = "[[0]]"
        self.assertEqual(u.rollDice(self.msg), "I can't roll a die with 0 sides!")

        self.msg.content = "[[-1]]"
        self.assertEqual(u.rollDice(self.msg), "I can't roll a die with -1 sides!")

        self.msg.content = "[[1001]]"
        self.assertEqual(u.rollDice(self.msg), "I can't roll a die with 1001 sides!")

        self.msg.content = "[[words]]"
        self.assertEqual(u.rollDice(self.msg), "I can't roll a die with words sides!")

        self.msg.content = "[[1.5]]"
        self.assertEqual(u.rollDice(self.msg), "I can't roll a die with 1.5 sides!")

        self.msg.content = "[[5]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[50]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[500]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

        self.msg.content = "[[1000]]"
        self.assertIn("You rolled", u.rollDice(self.msg))

if __name__ == "__main__":
    unittest.main()
