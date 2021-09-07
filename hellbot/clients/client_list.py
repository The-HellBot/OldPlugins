from .session import Hell, H2, H3, H4, H5
from hellbot.config import Config


async def clients_list(Config, Hell, H2=None, H3=None, H4=None, H5=None):
    user_ids = list(Config.SUDO_USERS) or ''
    main_id = await Hell.get_me()
    user_ids.append(main_id.id)
    if H2 is not None:
        id2 = await H2.get_me()
        user_ids.append(id2.id)
    if H3 is not None:
        id3 = await H3.get_me()
        user_ids.append(id3.id)
    if H4 is not None:
        id4 = await H4.get_me()
        user_ids.append(id4.id)
    if H5 is not None:
        id5 = await H5.get_me()
        user_ids.append(id5.id)
    return user_ids
