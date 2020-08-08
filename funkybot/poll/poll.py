#==== Description ====
"""
Keeps track of active polls
"""

#==== Imports ====
from funktions import constant as c

#==== Globals ====


#==== Poll class ====
class Poll():
    def __init__(self,author,question,options):
        self.author = author
        self.question = question
        self.options = self.__formatOptions(options)
        if self.options != None:
            self.body = self.__formatBody()

    def __formatOptions(self,optList):
        optDict = {}    

        for o in range(len(optList)):
            optDict[chr(0x1f1e6 + o)] = optList[o]

        return optDict

    def __formatBody(self):
        self.question = self.question.lstrip()
        if self.question != "":
            self.question = "\n\n" + self.question + "\n"
        body = c.POLL_START % self.author.display_name + self.question

        for o in self.options:
            body = body + "\n" + "{} - {}".format(o, self.options[o])

        return body

