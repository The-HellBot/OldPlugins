from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (ChannelParticipantAdmin,
                               ChannelParticipantCreator)


# Check if Admin
async def is_admin(client, chat_id, user_id):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        hellboy = await client(GetParticipantRequest(channel=chat_id, user_id=user_id))
        chat_participant = hellboy.participant
        if isinstance(chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return True
    except Exception:
        return False
    else:
        return False


# hellbot
