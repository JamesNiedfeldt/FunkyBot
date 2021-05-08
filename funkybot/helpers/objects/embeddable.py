#==== Description ====
"""
Encapsulates all necessary information for Discord embeds
"""

#==== Embeddable class ====
class Embeddable():
    def __init__(self, url="", title="", text="", image=""):
        self.url = url
        self.title = title
        self.description = text
        self.image = {"url": image}
        self.footer = None
        self.fields = []
        self.color = 2303786
        self._empty = False

    def setColor(self, color):
        if isinstance(color, int):
            self.color = color

    def setThumbnail(self, image):
        self.thumbnail = {"url": image}

    def setFooter(self, text):
        self.footer = {"text": text}

    def addField(self, *fields):
        for f in fields:
            self.fields.append(f)

    def asDict(self):
        return self.__dict__

    def empty(self):
        return self._empty

def empty(message):
    embed = Embeddable(text=message)
    embed._empty = True

    return embed
        
    
