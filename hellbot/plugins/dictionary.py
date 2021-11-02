import aiohttp

# from PyDictionary import PyDictionary

from . import *


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()


@hell_cmd(pattern="ud ([\s\S]*)")
async def _(event):
    word = event.text[4:]
    try:
        response = await AioHttp().get_json(
            f"http://api.urbandictionary.com/v0/define?term={word}",
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        result = f"**Text : {word}**\n**Meaning :**\n`{definition}`\n\n**Example :**\n`{example}`"
        await eor(event, result)
    except Exception as e:
        await eod(event, f"**Error !!** \n\n`{e}`")


"""
@hell_cmd(pattern="meaning (.*)")
async def _(event):
    word = event.pattern_match.group(1)
    dictionary = PyDictionary()
    hell = dictionary.meaning(word)
    output = f"**Word :** __{word}__\n\n"
    try:
        for a, b in hell.items():
            output += f"**{a}**\n"
            for i in b:
                output += f"☞ __{i}__\n"
        await eor(event, output)
    except Exception:
        await eod(event, f"Couldn't fetch meaning of {word}")
"""

CmdHelp("dictionary").add_command(
  'ud', 'query', 'Fetches meaning of given word from Urban Dictionary.'
).add_info(
  'Dictionary 📕'
).add_warning(
  '✅ Harmless Module.'
).add()
