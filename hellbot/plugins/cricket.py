import urllib.request
from bs4 import BeautifulSoup
from . import *


@bot.on(hell_cmd(pattern="cs$"))
@bot.on(sudo_cmd(pattern="cs$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = ""
    for match in result:
        Sed += match.get_text() + "\n\n"
    await event.edit(
        f"<b><u>Match information gathered successful</b></u>\n\n\n<code>{Sed}</code>",
        parse_mode="HTML",
    )


CmdHelp("cricket").add_command(
  "cs", None, "Collects all the live cricket scores."
).add_info(
  "Cricket Kheloge Vro?"
).add_warning(
  "✅ Harmless Module."
).add()
