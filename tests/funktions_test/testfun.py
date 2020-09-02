import unittest
import discord
from funktions_test import mockmessage as m
from funktions import fun as f, helpers as h, constant as c

class TestFun(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = m.MockMessage()
    
    def test_eightBall(self):
        self.assertIsNotNone(f.eightBall())

    def test_choose(self):
        self.msg.content = "[[x|y]]"
        self.assertIn(f.choose(self.msg), ["I choose x!","I choose y!"])

        self.msg.content = "[[x]]"
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_TOO_FEW))

        self.msg.content = "[[a|b|c|d|e|f|g|h|i|j|k]]"
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_TOO_MANY))

        self.msg.content = "[[x|y]"
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_BRACKETS))

        self.msg.content = "[x|y]]"
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_BRACKETS))

        self.msg.content = "[[]]"
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_TOO_FEW))

        self.msg.content = ""
        self.assertEqual(f.choose(self.msg), h.badArgs("choose", c.ERR_BRACKETS))

    def test_findOneLiner(self):
        self.assertIsNotNone(f.findOneLiner())

    def test_randomPic(self):
        self.assertIsNotNone(f.randomPic("reaction_pics"))

        self.assertIsNotNone(f.randomPic("cute_pics"))

        try:
            f.randomPic("test")
            self.fail("FileNotFoundError was not raised")
        except FileNotFoundError:
            pass

    def test_rateSomething(self):
        self.msg.content = "[[x]]"
        self.assertIn("I give x", f.rateSomething(self.msg))

        self.msg.content = "[[funkybot]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.content = "[[FUNKYBOT]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.content = "[[funky]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.content = "[[FUNKY]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.content = "[[you]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.content = "[[YOU]]"
        self.assertEqual(f.rateSomething(self.msg), "I give myself an 11/10. Literally the best ever.")

        self.msg.author.display_name = "test"
        self.msg.content = "[[me]]"
        self.assertIn("I give test", f.rateSomething(self.msg))

        self.msg.content = "[[ME]]"
        self.assertIn("I give test", f.rateSomething(self.msg))

        self.msg.content = "[[myself]]"
        self.assertIn("I give test", f.rateSomething(self.msg))

        self.msg.content = "[[MYSELF]]"
        self.assertIn("I give test", f.rateSomething(self.msg))

        self.msg.content = "[[x]"
        self.assertEqual(f.rateSomething(self.msg), h.badArgs("rate", c.ERR_BRACKETS))

        self.msg.content = "[x]]"
        self.assertEqual(f.rateSomething(self.msg), h.badArgs("rate", c.ERR_BRACKETS))

        self.msg.content = "[[]]"
        self.assertEqual(f.rateSomething(self.msg), h.badArgs("rate", c.ERR_TOO_FEW))

        self.msg.content = ""
        self.assertEqual(f.rateSomething(self.msg), h.badArgs("rate", c.ERR_BRACKETS))

        self.msg.content = "[[x|y]]"
        self.assertEqual(f.rateSomething(self.msg), h.badArgs("rate", c.ERR_TOO_MANY))

if __name__ == "__main__":
    unittest.main()
    
