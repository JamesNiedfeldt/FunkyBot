# FunkyBot

---
FunkyBot is a simple Discord bot with a variety of functions. It was created as a personal project and as such contains functionality catered towards a small group of people and is not available to be publically added via server invites. You are however free to use this code for your own personal server use or to modify.

---
### Requirements
FunkyBot requires Python-version 3.5 or newer to run. 

Additionally it requires the following modules, listed in `requirements.txt`. These can be automatically installed by running `pip install -r requirements.txt`.
- discord.py >= 1.3.4
- requests

Finally, certain files must exist within the project directory for FunkyBot to properly run, but are not and should not be included in the project repository. These include:
- `funkybot/files/token.txt`
    This must contain a single line containing only your app's login token, found on its app page in the Discord Developer Portal.

- `funkybot/files/user_agent.txt`
    This must contain two lines containing only your name and email. This is used for HTTP request headers in order to identify the user of the bot. For example, this file should look like:
    ```
    Firstname Lastname
    email@example.com
    ```
- Reaction images/shiba images
    The two image folders (`funkybot/files/reaction_pics` and `funkybot/files/shiba_pics`) should contain images for their respective commands to randomly choose from. If either folder contain no images, the commands will work but return a message stating there was nothing to find.

---
### Running FunkyBot
When the necessary packages have been installed and additional files have been placed in their required places, FunkyBot can be run using `python3 funkybot.py`. 