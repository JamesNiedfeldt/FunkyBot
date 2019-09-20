#Mock the discord.Message object

class MockMessage():
    def __init__(self):
        self.message = ""
        self.author = type("author", (), {"display_name" : ""})
