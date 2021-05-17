import os
os.system("pip install telethon")
import telethon
from telethon.sessions import StringSession
from telethon.sync import TelegramClient


okvai = input("Enter 69 to continue: ")
if okvai == "69":
    print("Please go to my.telegram.org and get your API Id and API Hash to proceed.")
    APP_ID = int(input("Enter APP ID here: "))
    API_HASH = input("Enter API HASH here: ")

    with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
        print(client.session.save())
        client.send_message("me", client.session.save())
        client.send_message("me", "Above is your #HELLBOT_SESSION \nPaste this string in Heroku Var.\n\n[Team HellBot](t.me/the_hellbot)")

else:
    print("Bhag jaa bhosdike")
