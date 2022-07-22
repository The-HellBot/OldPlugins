# EDIT THIS FILE AND RENAME TO config.py TO MAKE THIS BOT WORKING
# FILL THESE VALUES ACCORDINGLY.

from hellbot.config.hell_config import Config

class Development(Config):
  # get these values from my.telegram.org. 
  ENV = "ANYTHING"

ABUSE = "ON"

HANDLER = "."

APP_ID = "2791256"

API_HASH = "cd2fb4cdc795334aee3fbbc83da463ce"

BOT_TOKEN = "5006643023:AAFuiTBrxHQWRNAO6i-XKCe0mQ4zlg6RtDM"

HELLBOT_SESSION = ""

  # create any PostgreSQL database.
  # I recommend to use elephantsql and paste that link here
  DB_URI = "mongodb+srv://erichdaniken:erichdaniken@cluster0.c13qk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

  # After cloning the repo and installing requirements...
  # Do `python string.py` and fill the on screen prompts.
  # String session will be saved in your saved message of telegram.
  # Put that string here.

  # Create a bot in @BotFather
  # And fill the following values with bot token and username.

  # Custom Command Handler. 
  HANDLER = "."

  # Custom Command Handler for sudo users.
  SUDO_HANDLER = "!"


# end of required config
# hellbot
