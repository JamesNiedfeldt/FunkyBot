import unittest
import discord
from funktions_test import mockmessage as m
from funktions import helpers as h

class TestHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = ""

    def test_parse(self):
        self.msg = "[[]]"
        self.assertEquals(h.parse(self.msg), [])

        self.msg = "[[x|]]"
        self.assertEquals(h.parse(self.msg), [])

        self.msg = "[[x]]"
        self.assertEquals(h.parse(self.msg), ['x'])

        self.msg = "[[x|y]]"
        self.assertEquals(h.parse(self.msg), ['x', 'y'])

if __name__ == "__main__":
    unittest.main()
    
