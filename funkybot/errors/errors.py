#==== Description ====
"""
Contains custom exceptions for FunkyBot
"""

#==== Base Error class ====
class Error(Exception):
    pass

#==== Arguments formatted wrong ====
class BadArgumentException(Error):
    def __init__(self, command):
        self.errorCode = "brackets"
        self.command = command
        super().__init__()

#==== At least one empty argument ====
class EmptyArgumentException(Error):
    def __init__(self, command):
        self.errorCode = "empty"
        self.command = command
        super().__init__()

#==== Too few arguments ====
class TooFewArgumentsException(Error):
    def __init__(self, command):
        self.errorCode = "too_few"
        self.command = command
        super().__init__()

#==== Too many arguments ====
class TooManyArgumentsException(Error):
    def __init__(self, command):
        self.errorCode = "too_many"
        self.command = command
        super().__init__()

#==== Invalid value for a number argument ====
class BadValueException(Error):
    def __init__(self, command):
        self.errorCode = "bad_value"
        self.command = command
        super().__init__()

#==== Number too high or low for number argument ====
class BadNumberException(Error):
    def __init__(self, command):
        self.errorCode = "bad_number"
        self.command = command
        super().__init__()

#==== Custom exception ====
class CustomCommandException(Error):
    def __init__(self, command, errorCode):
        self.errorCode = errorCode
        self.command = command
        super().__init__()
    
