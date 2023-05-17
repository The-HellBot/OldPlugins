import os


class Config(object):
    # Editable Variables #
    ABUSE = os.environ.get("ABUSE", None)
    API_HASH = os.environ.get("API_HASH", None)
    APP_ID = os.environ.get("APP_ID", None)
    BL_CHAT = set(int(x) for x in os.environ.get("BL_CHAT", "").split())
    BOT_HANDLER = os.environ.get("BOT_HANDLER", "\/")
    BOT_LIBRARY = os.environ.get("BOT_LIBRARY", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    BUTTONS_IN_HELP = int(os.environ.get("BUTTONS_IN_HELP", 7))
    CURRENCY_API = os.environ.get("CURRENCY_API", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    EMOJI_IN_HELP = os.environ.get("EMOJI_IN_HELP", "✧")
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
    GIT_REPO_NAME = os.environ.get("GIT_REPO", None)
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)
    HANDLER = os.environ.get("HANDLER", ".")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    IG_SESSION = os.environ.get("INSTAGRAM_SESSION", None)
    INSTANT_BLOCK = os.environ.get("INSTANT_BLOCK", None)
    LOGGER_ID = int(os.environ.get("LOGGER_ID", 0))
    LYRICS_API = os.environ.get("LYRICS_API", None)
    MAX_SPAM = int(os.environ.get("MAX_SPAM", 3))
    MY_CHANNEL = os.environ.get("YOUR_CHANNEL", "Its_HellBot")
    MY_GROUP = os.environ.get("YOUR_GROUP", "HellBot_Chat")
    OCR_API = os.environ.get("OCR_API", None)
    PLUGIN_CHANNEL = int(os.environ.get("PLUGIN_CHANNEL", 0))
    PM_LOGGER = int(os.environ.get("PM_LOGGER", 0))
    PM_PERMIT = os.environ.get("PM_PERMIT", "True")
    REMOVE_BG_API = os.environ.get("REMOVE_BG_API", None)
    HELLBOT_SESSION = os.environ.get("HELLBOT_SESSION", None)
    SESSION_2 = os.environ.get("SESSION_2", None)
    SESSION_3 = os.environ.get("SESSION_3", None)
    SESSION_4 = os.environ.get("SESSION_4", None)
    SESSION_5 = os.environ.get("SESSION_5", None)
    SHORTENER_API = os.environ.get("SHORTENER_API", None)
    SUDO_HANDLER = os.environ.get("SUDO_HANDLER", ".")
    TAG_LOGGER = int(os.environ.get("TAG_LOGGER", 0))
    THUMB_IMG = os.environ.get("THUMB_IMG", "./HellConfig/resources/pics/hellbot_logo.jpg")
    UNLOAD = list(os.environ.get("UNLOAD", "").split())
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/The-HellBot/HellBot")
    UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "master")
    WEATHER_API = os.environ.get("WEATHER_API", None)

    # Don't edit variables below this line #
    LOGGER = True
    CHROME_BIN = os.environ.get("CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/app/.chromedriver/bin/chromedriver")
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
    MAX_MESSAGE_SIZE_LIMIT = 4095
    SUDO_USERS = []
    TELEGRAPH_NAME = os.environ.get("TELEGRAPH_NAME", "[ †he Hêllẞø† ]")
    TEMP_DIR = os.environ.get("TEMP_DIR", None)
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
    


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
