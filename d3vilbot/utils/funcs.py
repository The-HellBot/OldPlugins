import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from d3vilbot import *
from d3vilbot.helpers import *
from d3vilbot.config import Config


# just a small shit for big works
class Loader:
    def __init__(self, func=None, **args):
        self.Var = Var
        bot.add_event_handler(func, events.NewMessage(**args))


# Check if Admin
async def is_admin(client, chat_id, user_id):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        d3vilboy = await client(GetParticipantRequest(channel=chat_id, user_id=user_id))
        chat_participant = d3vilboy.participant
        if isinstance(
            chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
        ):
            return True
    except Exception:
        return False
    else:
        return False

# d3vilbot
