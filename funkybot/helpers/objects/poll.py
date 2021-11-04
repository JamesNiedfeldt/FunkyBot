#==== Description ====
"""
Keeps track of active polls
"""

#==== Imports ====
from helpers import constant as c, global_vars as g, helper_functions as h

#==== Poll class ====
class Poll():
    def __init__(self,msg,question,options):
        self.author = h.escapeCodeBlock(msg.author.display_name)
        self.question = question
        self.options = self.__formatOptions(options)
        if self.options != None:
            self.body = self.__formatBody()
        self.messageId = None
        self.activeId = str(msg.author.id) + "|" + str(msg.channel.id)

    def __formatOptions(self,optList):
        optDict = {}    

        for o in range(len(optList)):
            optDict[chr(0x1f1e6 + o)] = h.escapeCodeBlock(optList[o])

        return optDict

    def __formatBody(self):
        self.question = " ".join(self.question.split())
        if self.question == "":
            self.question = "*No question was given*"
        self.question = self.question + "\n"
        body = c.POLL_START % (
            h.pluralize(g.props['poll_run_duration'], "hour"), self.author)
        body = body + c.LINE_BREAK + self.question

        for o in self.options:
            body = body + "\n" + "{} - {}".format(o, self.options[o])

        return body

