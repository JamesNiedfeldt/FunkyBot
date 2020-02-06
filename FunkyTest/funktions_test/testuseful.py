import unittest
from funktions_test import mockmessage as m
from funktions import helpers as h
from funktions import useful as u

class TestUseful(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.msg = m.MockMessage()

    def test_toBin(self):
        #self.msg.content = "[[0]]"
        #self.assertEqual(u.toBin(self.msg), "0")

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
        #self.msg.content = "[[0]]"
        #self.assertEqual(u.toHex(self.msg), "0")

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

if __name__ == "__main__":
    unittest.main()
