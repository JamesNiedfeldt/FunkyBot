#Mock the discord.Message object

class MockMessage():
    def __init__(self):
        self.content = ""
        self.author = type("author", (), {"display_name" : "", "name": ""})
        self.server = ""
        self.channel = ""
        self.timestamp = ""
