#==== Description ====
"""
Encapsulates all necessary information for Discord embeds
"""

#==== Imports ====

#==== Timer class ====
class Embeddable():
    def __init__(self, url, title, text, image):
        self.url = url
        self.title = title
        self.text = text
        self.image = image
        self._empty = False

    def empty(self):
        return self._empty

def empty(message):
    embed = Embeddable(None, None, message, None)
    embed._empty = True

    return embed
        
    
