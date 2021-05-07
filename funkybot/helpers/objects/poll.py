#==== Description ====
"""
Keeps track of active polls
"""

#==== Imports ====
from helpers import constant as c

#==== Poll class ====
class Poll():
    def __init__(self,author,question,options):
        self.author = author.display_name
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
        self.question = " ".join(self.question.split())
        if self.question == "":
            self.question = "*No question was given*"
        self.question = self.question + "\n"
        body = (c.POLL_START + c.LINE_BREAK) % self.author + self.question

        for o in self.options:
            body = body + "\n" + "{} - {}".format(o, self.options[o])

        return body

