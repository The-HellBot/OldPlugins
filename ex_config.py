# FOR SELF HOST
# EDIT THIS FILE AND RENAME TO config.py TO MAKE THIS BOT WORKING
# FILL THESE VALUES ACCORDINGLY.

from HellConfig.config import Config


class Development(Config):
    # get these values from my.telegram.org.
    
    APP_ID = 666666  # 666666 is a placeholder. Fill your 6 digit api id
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"  # replace this with your api hash
    BOT_TOKEN = "Your value"  # Create a bot from @BotFather and paste the token here
    BOT_LIBRARY = "telethon"  # fill 'pyrogram' if you want pyrogram version of hellbot else leave it as it is.
    DATABASE_URL = "Your value"  # A postgresql database url from elephantsql
    HELLBOT_SESSION = "Your value"  # telethon or pyrogram string according to BOT_LIBRARY
    HANDLER = "."  # Custom Command Handler
    SUDO_HANDLER = "!"  # Custom Command Handler for sudo users.


# end of required config
# hellbot
