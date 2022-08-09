from TelethonHell.utils.extras import delete_hell as eod
from TelethonHell.utils.extras import edit_or_reply as eor


class CancelProcess(Exception):
    """
    Cancel Process
    """


async def parse_error(event, error, auto_parse=True, delete=True, time=10):
    if delete:
        if auto_parse:
            await eod(event, f"**ERROR !!** \n\n`{error}`", time)
        else:
            await eod(event, f"**ERROR !!** \n\n{error}", time)
    else:
        if auto_parse:
            await eor(event, f"**ERROR !!** \n\n`{error}`")
        else:
            await eor(event, f"**ERROR !!** \n\n{error}")


# hellbot
