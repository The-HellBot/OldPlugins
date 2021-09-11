import telethon.utils


@hell_cmd(pattern="ping$")
async def _(event):
    client.me = await event.client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)
    ForGo10God = client.uid
    HELL_USER = client.me.first_name
    await eor(event, f"Pong \n\n{ForGo10God}\n\n{HELL_USER}")
