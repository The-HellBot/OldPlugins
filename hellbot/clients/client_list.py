from hellbot import bot
from hellbot.clients import Hell, H2, H3, H4, H5
from hellbot.config import Config


async def clients_list(Config, Hell, H2, H3, H4, H5):
    user_ids = []
    if Config.SUDO_USERS:
        user_ids.append(list(Config.SUDO_USERS))
    main_id = await bot.get_me()
    user_ids.append(main_id.id)
    if H2:
        id2 = await H2.get_me()
        user_ids.append(id2.id)
    if H3:
        id3 = await H3.get_me()
        user_ids.append(id3.id)
    if H4:
        id4 = await H4.get_me()
        user_ids.append(id4.id)
    if H5:
        id5 = await H5.get_me()
        user_ids.append(id5.id)
    return user_ids
