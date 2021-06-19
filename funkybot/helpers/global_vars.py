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

"""
These are changed after initialization to make !react
and !cute appear more random
"""
#Last sent cute/react pics
recentCute = []
recentReact = []

