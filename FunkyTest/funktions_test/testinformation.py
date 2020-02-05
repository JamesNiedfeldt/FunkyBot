import unittest
from funktions import information as i
from funktions import helpers as h

class TestInformation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_commandList(self):
        self.assertIsNotNone(i.commandList())

    def test_sayHello(self):
        sender = type("sender", (), {"display_name" : ""})

        sender.display_name = "Test Name"
        version = "x.y.z"
        time = h.formatTime(0)
        msg = """
    Hello %s, my name is FunkyBot! I am a simple bot made for fun as my creator's personal project. Here's some information about me:

    **Current version:** %s
    **Current uptime:** %s
    """ % (sender.display_name, version, time)
        self.assertEqual(i.sayHello(sender, "x.y.z", h.getTime()), msg)

if __name__ == "__main__":
    unittest.main()
