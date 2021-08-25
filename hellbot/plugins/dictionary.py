from PyDictionary import PyDictionary

from . import *


@bot.on(admin_cmd(pattern="meaning (.*)"))
@bot.on(sudo_cmd(pattern="meaning (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    word = event.pattern_match.group(1)
    dictionary = PyDictionary()
    hell = dictionary.meaning(word)
    output = f"**Word :** __{word}__\n\n"
    try:
        for a, b in hell.items():
            output += f"**{a}**\n"
            for i in b:
                output += f"☞ __{i}__\n"
        await edit_or_reply(event, output)
    except Exception:
        await edit_or_reply(event, f"Couldn't fetch meaning of {word}")


CmdHelp("dictionary").add_command(
  'meaning', 'query', 'Fetches meaning of the given word'
).add_info(
  'Dictionary 📕'
).add_warning(
  '✅ Harmless Module.'
).add()
