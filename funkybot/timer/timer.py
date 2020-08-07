#==== Description ====
"""
Acts as a timer for other tasks
"""

#==== Imports ====
import asyncio
import time

#==== Timer class ====
class Timer():
    #Let the timer run until given datetime
    async def timeUntilDate(self,date):
        done = False

        while not done:
            if time.time() >= date:
                done = True
            else:
                await asyncio.sleep(1)

    #Let the timer run for given duration in seconds
    async def timeForDuration(self,duration):
        await asyncio.sleep(duration)
        
    
