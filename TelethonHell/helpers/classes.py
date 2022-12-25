import aiohttp


# class for afk to create separate afk objects for each client
class AFK:
    def __init__(self):
        self.afk_end = {}
        self.afk_pic = None
        self.afk_start = {}
        self.afk_time = None
        self.last_message = {}
        self.reason = None


# class for filter to create separate filter objects for each client
class FILTER:
    def __init__(self):
        self.last_triggered_filters = {}


# an aiohttp session class
class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()


# class for pmpermit to create separate pmpermit objects for each client
class PM_PERMIT:
    def __init__(self):
        self.PM_WARNS = {}
        self.PREV_REPLY_MESSAGE = {}


# class for spam module
class SPAM:
    def __init__(self):
        self.spam = False
        self.chat = None


# class for stickers
class STICKER:
    def __init__(self):
        self.emoji = "🍀"
        self.pack = 1