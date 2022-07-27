import requests

from . import *


@hell_cmd(pattern="ytube(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://www.youtube.com/results?search_query={}".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me **UThoob** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


@hell_cmd(pattern="ddg(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://duckduckgo.com/?q={}&t=h_&ia=about".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me **duckduckgo** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


@hell_cmd(pattern="altn(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://www.altnews.in/?s={}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me **altnews** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


@hell_cmd(pattern="lmkp(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://indiankanoon.org/search/?formInput={}+sortby%3Amostrecent".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me **Indiankanoon.com : Place** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


@hell_cmd(pattern="gem(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://mkp.gem.gov.in/search?q={}&sort_type=created_at_desc&_xhr=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me **gem.gov.in** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


@hell_cmd(pattern="rchiv(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://web.archive.org/web/*/{}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "Let me run your link on wayback machine that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            ),
        )
    else:
        await eod(event, "Something went wrong. Please try again later.")


CmdHelp("search").add_command(
    "rchiv", "<query>", "Gives you the archive link of given query from WayBack Machine"
).add_command(
    "gem", "<query>", "Gives you the link of given query from Government e-Marketplace (gem.gov.in)"
).add_command(
    "lmkp", "<query>", "Gives you the link of given query from Indiankanoon.org"
).add_command(
    "ytube", "<query>", "Gives you the link of given query from youthube"
).add_command(
    "altn", "<query>", "Gives you the link for given query from Alt News"
).add_command(
    "ddg", "<query>", "Gives you the link for given query from Duckduckgo"
).add_info(
    "Another Search Module."
).add_warning(
    "✅ Harmless Module."
).add()
