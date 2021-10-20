import urllib.request

from bs4 import BeautifulSoup

from . import *


@hell_cmd(pattern="cs$")
async def _(event):
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    final = ""
    for match in result:
        final += match.get_text() + "\n\n"
    await eor(event, f"<b><i><u>Match information gathered successful</b></i></u>\n\n<code>{final}</code>", parse_mode="HTML")


CmdHelp("cricket").add_command(
  "cs", None, "Collects all the live cricket scores."
).add_info(
  "Cricket Kheloge Vro?"
).add_warning(
  "✅ Harmless Module."
).add()
