#==== Description ====
"""
Contains global variables, initialized at startup
These should not be changed after startup
"""

#Discord client
client = None

#Properties from conf file
props = {}

#Headers for API requests
apiHeaders = {}

#Startup time
begin = None

#Denylist
denylist = []

#Database
db = None

#Active reminders
reminders = []

#List of active polls
activePolls = []

#List of common mistakes for command suggestions
commonMistakes = {}

"""
These are changed after initialization to track runtime changes
"""
#Last sent cute/react pics
recentCute = []
recentReact = []

#Lifetime commands used
totalCommands = -1

