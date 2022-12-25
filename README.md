<h1 align="center">
  <b>†hê Hêllẞø† 🇮🇳</b>
</h1>

<p align="center">
  <img src="https://te.legra.ph/file/fd0c3c2201447746fd1d0.jpg" alt="The-HellBot">
</p>

<h6 align="center">
  <b>⚡ ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt ⚡</b>
</h6>

<h3 align="center">
  <b>A Smooth & Fast Telegram Userbot Based On Telethon Bot Library.</b>
</h3>

-----

<details><summary><h1><b>Deploy Alternatives 🥷🏻</h1></b></summary>

  - 
    [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/The-HellBot/Plugins-T&branch=master&name=hellbot-koyeb&run_command=bash+runkoyeb&env[APP_ID]&env[API_HASH]&env[BOT_TOKEN]&env[HELLBOT_SESSION]&env[DATABASE_URL])

</details>

-----

<h1 align="center">
  <b>Follow this format to make your own plugin for HellBot</b>
</h1>

```python3
"""
A sample code to display hello without taking input.
"""
# this is a mandatory import
from . import *

# assigning command
@hell_cmd(pattern="hii$")
async def hi(event):
    # command body
    await eor(event, "Hello!")


# to display in help menu
CmdHelp("hii").add_command(
  "hii", None, "Says Hello!"
).add()
```
----
```python3
"""
A sample code to display hello with input.
"""
# this is a mandatory import
from . import *

# assigning command
@hell_cmd(pattern="hii(?:\s|$)([\s\S]*)")
async def hi(event):
    # command body
    _input = event.pattern_match.group(1)
    if _input:
        await eor(event, f"Hello! {_input}")
    else:
        await eor(event, "Hello!")


# to display in help menu
CmdHelp("hii").add_command(
    "hii", "<text>", "Display Hello with a input!"
).add()
```


### To get more functions read codes in repo.

------

## Disclaimer
- We won't be responsible for any kind of ban due to this bot.
- HellBot was made for fun purpose and to make group management easier.
- It's your concern if you spam and gets your account banned.
- Also, Forks won't be entertained.
- If you fork this repo and edit plugins, it's your concern for further updates.
- Forking Repo is fine. But if you edit something we will not provide any help.
- In short, Fork At Your Own Risk.

------
# License

![](https://www.gnu.org/graphics/gplv3-or-later.png)

<h4 align="center">Copyright (C) 2022 <a href="https://github.com/The-HellBot">The-HellBot</a></h4>

Project [HellBot](https://github.com/The-HellBot/HellBot) is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

------
## Credits

- 💖 [Telethon](https://github.com/LonamiWebs/Telethon)
- 💖 [Pyrogram](https://github.com/Pyrogram/Pyrogram)
- 💖 Team Hellbot

------
