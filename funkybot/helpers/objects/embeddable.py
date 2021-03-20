#==== Description ====
"""
Encapsulates all necessary information for Discord embeds
"""

#==== Embeddable class ====
class Embeddable():
    def __init__(self, url=None, title=None, text=None, image=None, footer=None):
        self.url = url
        self.title = title
        self.text = text
        self.image = image
        self.footer = footer
        self._empty = False

    def empty(self):
        return self._empty

def empty(message):
    embed = Embeddable(text=message)
    embed._empty = True

    return embed
        
    
