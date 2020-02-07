#Mock the discord.Message object

class MockMessage():
    def __init__(self):
        self.content = ""
        self.author = type("author", (), {"display_name" : "", "name": "",
                                          "mention" : ""})
        self.server = ""
        self.channel = type("channel", (), {"name" : "", "id": -1})
        self.timestamp = ""
