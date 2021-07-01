# EDIT THIS FILE AND RENAME TO config.py TO MAKE THIS BOT WORKING
# FILL THESE VALUES ACCORDINGLY.

from hell_config import Config

class Development(Config):
  # get these values from my.telegram.org. 
  APP_ID = 6    # 6 is a placeholder. Fill your 6 digit api id
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"   # replace this with your api hash

  # the name to display in your alive message.
  # If not filled anything then default value is I'm Hêll.
  YOUR_NAME = "I'm Hêll"

  # create any PostgreSQL database.
  # I recommend to use elephantsql and paste that link here
  DB_URI = "Your value"

  # After cloning the repo and installing requirements...
  # Do `python string.py` and fill the on screen prompts.
  # String session will be saved in your saved message of telegram.
  # Put that string here.
  HELLBOT_SESSION = "Your value"

  # Create a bot in @BotFather
  # And fill the following values with bot token and username.
  BOT_TOKEN = "Your value" #token
  BOT_USERNAME = "Your value" #username

  # Create a private group and add rose bot to it.
  # and type /id and paste that id here.
  # replace that -100 with that group id.
  LOGGER_ID = -100

  # Custom Command Handler. 
  HANDLER = "."

  # enter the userid of sudo users.
  # you can add multiple ids by separating them by space.
  # fill values in [] only.
  SUDO_USERS = []

  # Custom Command Handler for sudo users.
  SUDO_HANDLER = "!"

# end of required config
# hellbot
