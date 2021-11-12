# FunkyBot

---
FunkyBot is a simple Discord bot with a variety of functions. It was created as a personal project and as such contains functionality catered towards a small group of people and is not available to be publically added via server invites. You are however free to use this code for your own personal server use or to modify.

---
### Requirements
FunkyBot requires Python-version 3.5 or newer to run. 

Additionally it requires the following modules, listed in `requirements.txt`. These can be automatically installed by running `pip install -r requirements.txt`.
- discord.py >= 1.7.0
- requests

Finally, certain files must exist within the project directory for FunkyBot to properly run, but are not and should not be included in the project repository. These include:
- `funkybot/files/funkybot.conf`
  - This contains certain properties required for FunkyBot to run. See below what properties are in this file. 
  - `funkybot/files/funkybot.conf.sample` contains an example of this file.
- `funkybot/files/denylist.xml`
  - This file must contain any Discord user IDs of users you don't want to use the bot enclosed in a `user` tag. There do not need to be any IDs, but the file must still contain the root XML tags found in the sample file.
  - `funkybot/files/denylist.xml.sample` contains an example of this file.
- Reaction images/cute images
  - The two image folders (`funkybot/files/reaction_pics` and `funkybot/files/cute_pics`) should contain images for their respective commands to randomly choose from. If either folder contain no images, the commands will work but return a message stating there was nothing to find.

---
### FunkyBot.conf
New in version 2.0.0 is the `funkybot/files/funkybot.conf` file, which contains either properties for making FunkyBot run (user token, API key, etc) or for customizing certain command's outputs. Missing properties will result in FunkyBot being unable to start. An example of a valid configuration file can be found at `files/funkybot.conf.sample.` Here are all of the properties, what they do, and what values they can have:
- `token`
  - This is the login token found in the Discord Developer Portal. Required for FunkyBot to communicate with Discord's API.
- `request_name`
  - This is your name which will be attached to API request headers in order to achieve best practice when making API requests. This is required even if all request-related commands are disabled, but it won't be used anywhere in that case.
- `request_email`
  - This is your email which will be attached to API request headers in order to achieve best practice when making API requests. This is required even if all request-related commands are disabled, but it won't be used anywhere in that case.
- `giantbomb_key`
  - This is your Giant Bomb API key required for making API requests using the `!game` command. If that command is disabled, this property may be left blank.
- `reset_command_usage`
  - Sets whether to clear command usage stats from the database at startup. If set to true, FunkyBot will "start fresh" recording command statistics for the `!hello` command when it starts up, as if no commands had ever been called. This must either be set to `true` or `false`.
- `poll_pin`
  - Sets whether FunkyBot will attempt to pin polls as long as they run. Regardless of this setting, FunkyBot will attempt to unpin polls that can't be finished due to a restart. This must either be set to `true` or `false`.
- `cute_delete`
  - Sets whether messages calling the `!cute` command should be deleted if FunkyBot has permissions to do so. This must either be set to `true` or `false`.
- `react_delete`
  - Sets whether messages calling the `!react` command should be deleted if FunkyBot has permissions to do so. This must either be set to `true` or `false`.
- `roll_max_args`
  - Sets the maximum number of arguments allowed in the `!roll` command. This must be an integer min 1 and max 10.
- `choose_max_args`
  - Sets the maximum number of arguments allowed in the `!choose` command. This must be an integer min 2 and max 10.
- `binary_max_args`
  - Setss the maximum number of arguments allowed in the `!binary` command. This must be an integer min 1 and max 10.
- `hex_max_args`
  - Sets the maximum number of arguments allowed in the `!hex` command. This must be an integer min 1 and max 10.
- `time_max_duration`
  - Sets the maximum duration a reminder set with the `!time` command can run, in days. This must be an integer min 1 and max 30.
- `poll_run_duration`
  - Sets the time a poll started with the `!poll` command will run before automatically closing, in hours. This must be an integer min 1 and max 10.
- `magic_currency`
  - Sets the currency used when displaying card prices via the `!magic` command. This can only be `usd`, `eur`, or `tix`.
- `magic_ignore_digital`
  - Sets whether the `!magic` command will ignore digital printings of cards. If set to `true` and the command finds a digital printing, it will attempt to find a non-digital print of the same card. If it can't find one or a digital set was specified, then the original card that was fetched will be sent. This must either be set to `true` or `false`.
- `debug`
  - Sets whether FunkyBot will print exceptions to stderr. Regardless of this setting, FunkyBot will write exceptions to the logs in `files/logs/`. This must either be set to `true` or `false`.
##### Disabling commands
You can also disable commands via the `files/funkybot.conf` file. To do so, add a property with the command's call (no `!` prefix), and set that property to `false`. By default, the `files/funkybot.conf.sample` file contains properties for `announce`, `magic`, `wiki`, and `game` all set to true. This is for convenience as these commands either use API calls or tag everyone, and thus are likely candidates for disabling.

Commands *do not* have to be listed to be enabled. If no property with a command's name is in the config file, it will be enabled by default. If a property is listed in the config file and is set to `true`, this is redundant.

---
### Note about FunkyBot API calls
The `!game`, `!magic`, and `!wiki` commands all fetch data via the [Giant Bomb API](https://www.giantbomb.com/api/), [Scryfall API](https://scryfall.com/docs/api), and [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) respectively. 

Scryfall and MediaWiki rate limits are generous enough that FunkyBot under normal use shouldn't be able to exceed them. However, the Giant Bomb API has a rate limit of 200 requests per hour, and each use of the `!game` command typically makes two API calls, effectively reducing the limit to 100 calls of the `!game` command per hour. In the future this may be adjusted to try to improve the amount of requests required by this command, but for now if this becomes a problem it is highly recommended to disable the `!game` command.

---
### Running FunkyBot
When the necessary packages have been installed and additional files have been placed in their required places, FunkyBot can be run using `python3 funkybot.py`. 