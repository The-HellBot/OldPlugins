# FOR SELF HOST
# EDIT THIS FILE AND RENAME TO config.py TO MAKE THIS BOT WORKING
# FILL THESE VALUES ACCORDINGLY.

from HellConfig.config import Config


class Development(Config):
    # get these values from my.telegram.org.
    
    APP_ID = "17429069" # 666666 is a placeholder. Fill your 6 digit api id
    API_HASH = "dc1a8101cd63983a45ab832ff2bf5673"  # replace this with your api hash
    BOT_TOKEN = "6049789485:AAEjexSzMynfLZ90SxtOFqkxvm9-p9f-yvU"  # Create a bot from @BotFather and paste the token here
    BOT_LIBRARY = "telethon"  # fill 'pyrogram' if you want pyrogram version of hellbot else leave it as it is.
    DATABASE_URL = "postgres://gdclonwq:o3XJbKoRdJFT5Giihd4CKTHvHRqiCxK5@trumpet.db.elephantsql.com/gdclonwq"  # A postgresql database url from elephantsql
    HELLBOT_SESSION = "==helL1BVtsOIIBu2QaqlxHRhLY-zKGzrYxfAVuIHnVhrU0DfH0v1lEP_9KpPXMGyXHFk6r5sicEoe07DUsUOSKmFVUHofnwmk_fZ-EvSDJWm5XAL92LMWyBHGBDlHnhYU566BBr7du4LETaN2x0e91AAtqlmOmHcBAvrD7JeY3HUWfPLXa6mgJFtwmecVDPQOfkCKnFPgzJwO0CR3lqPhxQyJq-wS59VwCraqezbNsmPxWAdET-08Wz2RSbyeMpqT90iHbU3QXRi9mn-2D65khxEuZHxdt59zP5Gd9psnL58mbhBdBxsYQzd_MBgfLAazxAMUTJZfAdCvoApZmQO2_Iaddxs1ZyduYHVo=bot=="  # telethon or pyrogram string according to BOT_LIBRARY
    HANDLER = "."  # Custom Command Handler
    SUDO_HANDLER = "!"  # Custom Command Handler for sudo users.


# end of required config
# hellbot
