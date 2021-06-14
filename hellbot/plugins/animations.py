import asyncio
from collections import deque

from . import *

@bot.on(hell_cmd(pattern=r"boxs$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"boxs$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    event = await eor(event, "`boxs...`")
    deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
    for _ in range(999):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@bot.on(hell_cmd(pattern=r"rain$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"rain$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    event = await eor(event, "`Raining.......`")
    deq = deque(list("🌬☁️🌩🌨🌧🌦🌥⛅🌤"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@bot.on(hell_cmd(pattern=r"deploy$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"deploy$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 3
    animation_ttl = range(12)
    event = await eor(event, "`Deploying...`")
    animation_chars = [
        "**Heroku Connecting To Latest [Github Build](The-HellBot/HellBot)**",
        f"**Build started by user** {hell_mention}",
        f"**Deploy** `535a74f0` **by user** **{hell_mention}**",
        "**Restarting Heroku Server...**",
        "**State changed from up to starting**",
        "**Stopping all processes with SIGTERM**",
        "**Process exited with** `status 143`",
        "**Starting process with command** `python3 -m stdborg`",
        "**State changed from starting to up**",
        "__INFO:Hêllẞø†:Logged in as 557667062__",
        "__INFO:Hêllẞø†:Successfully loaded all plugins__",
        "**Build Succeeded**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@bot.on(hell_cmd(pattern=r"dump$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"dump$", allow_sudo=True))
async def _(message):
    if event.fwd_from:
        return
    try:
        obj = message.pattern_match.group(1)
        if len(obj) != 3:
            raise IndexError
        inp = " ".join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    event = await eor(message, "`droping....`")
    u, t, g, o, s, n = inp.split(), "🗑", "<(^_^ <)", "(> ^_^)>", "⠀ ", "\n"
    h = [(u[0], u[1], u[2]), (u[0], u[1], ""), (u[0], "", "")]
    for something in reversed(
        [
            y
            for y in (
                [
                    "".join(x)
                    for x in (
                        f + (s, g, s + s * f.count(""), t),
                        f + (g, s * 2 + s * f.count(""), t),
                        f[:i] + (o, f[i], s * 2 + s * f.count(""), t),
                        f[:i] + (s + s * f.count(""), o, f[i], s, t),
                        f[:i] + (s * 2 + s * f.count(""), o, f[i], t),
                        f[:i] + (s * 3 + s * f.count(""), o, t),
                        f[:i] + (s * 3 + s * f.count(""), g, t),
                    )
                ]
                for i, f in enumerate(reversed(h))
            )
        ]
    ):
        for something_else in something:
            await asyncio.sleep(0.3)
            try:
                await event.edit(something_else)
            except errors.MessageIdInvalidError:
                return


@bot.on(hell_cmd(pattern=r"fleaveme$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"fleaveme$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(10)
    animation_chars = [
        "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
        "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
        "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
    ]
    event = await eor(event, "fleaveme....")
    await asyncio.sleep(2)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@bot.on(hell_cmd(pattern=r"loveu$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"loveu$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(70)
    event = await eor(event, "loveu")
    animation_chars = [
        "😀",
        "👩‍🎨",
        "😁",
        "😂",
        "🤣",
        "😃",
        "😄",
        "😅",
        "😊",
        "☺",
        "🙂",
        "🤔",
        "🤨",
        "😐",
        "😑",
        "😶",
        "😣",
        "😥",
        "😮",
        "🤐",
        "😯",
        "😴",
        "😔",
        "😕",
        "☹",
        "🙁",
        "😖",
        "😞",
        "😟",
        "😢",
        "😭",
        "🤯",
        "💔",
        "❤",
        "I Love You❤",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])


@bot.on(hell_cmd(pattern=r"plane$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"plane$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    event = await eor(event, "Wait for plane...")
    await event.edit("✈-------------")
    await event.edit("-✈------------")
    await event.edit("--✈-----------")
    await event.edit("---✈----------")
    await event.edit("----✈---------")
    await event.edit("-----✈--------")
    await event.edit("------✈-------")
    await event.edit("-------✈------")
    await event.edit("--------✈-----")
    await event.edit("---------✈----")
    await event.edit("----------✈---")
    await event.edit("-----------✈--")
    await event.edit("------------✈-")
    await event.edit("-------------✈")
    await asyncio.sleep(3)


@bot.on(hell_cmd(pattern=r"police$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"police$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(12)
    event = await eor(event, "Police")
    animation_chars = [
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])
        
@bot.on(hell_cmd(pattern=f"hack$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"hack$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(15)
    event = await eor(event, "`Hacking this kid....`")
    animation_chars = [
            "Looking for WhatsApp databases in targeted person...",
            " User online: True\nTelegram access: True\nRead Storage: True ",
            "Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 20s",
            "Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 18s",
            "Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 16s",
            "Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 14s",
            "Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 12s",
            "Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 10s",
            "Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 08s",
            "Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s",
            "Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 04s",
            "Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 02s",
            "Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s",
            "Hacking complete!\nUploading file...",
            "Targeted Account Hacked...!\n\n ✅ File has been successfully uploaded to my server.\nWhatsApp Database:\n`./DOWNLOADS/msgstore.db.crypt12`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 15])

@bot.on(hell_cmd(pattern=r"jio$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"jio$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(19)
    event = await eor(event, "jio network boosting...")
    animation_chars = [
        "`Connecting To JIO NETWORK ....`",
        "`█ ▇ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▇ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
        "*Optimising JIO NETWORK...*",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▒ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▇ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▇ █`",
        "**JIO NETWORK Boosted....**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 19])


@bot.on(hell_cmd(pattern=r"solarsystem$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"solarsystem$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(80)
    event = await eor(event, "solarsystem")
    animation_chars = [
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️🌎◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️◼️◼️◼️`",
        "`◼️🌕◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️☀◼️`",
        "`◼️◼️◼️🌕◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️☀◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️🌎◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️◼️◼️◼️`",
        "`◼️☀◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️🌕◼️`",
        "`◼️◼️◼️☀◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️🌕◼️◼️◼️`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])
        
        
@bot.on(hell_cmd(pattern="degi$"))
@bot.on(sudo_cmd(pattern="degi$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    event = await eor(event, "degi")
    await event.edit("WO")
    await asyncio.sleep(1.5)
    await event.edit("DegI")
    await asyncio.sleep(1.5)
    await event.edit("TuM")
    await asyncio.sleep(1.5)
    await event.edit("EkbaR")
    await asyncio.sleep(1.5)
    await event.edit("ManG")
    await asyncio.sleep(1.5)
    await event.edit("KaR")
    await asyncio.sleep(1.5)
    await event.edit("ToH")
    await asyncio.sleep(1.5)
    await event.edit("DekhO")
    await asyncio.sleep(1.5)
    await event.edit("Wo DeGi TuM eKbAr MaNg KaR tOh DeKhO😄")


@bot.on(hell_cmd(pattern=f"nehi$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"nehi$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    event = await eor(event, "nehi")
    await event.edit(
        "`Wo PaKkA DeGi Tu ManG KaR ToH DekH\n AuR NaA De To UskI BheN Ko PakaD😚😚`"
    )
    await asyncio.sleep(999)


@bot.on(hell_cmd(pattern="hnd (.*)"))
@bot.on(sudo_cmd(pattern="hnd (.*)", allow_sudo=True))
async def _(event):
    name = event.pattern_match.group(1)
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(6)
    event = await eor(event, "✌️")
    animation_chars = [
        "👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿                                          👈🏿\n👉🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👈🏿",
        "👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👉🏾                                  👈🏾\n👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾",
        "👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽\n👉🏽                        👈🏽\n👉🏽                        👈🏽\n👉🏽                        👈🏽\n👉🏽                        👈🏽\n👉🏽                        👈🏽\n👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽",
        "👇🏼👇🏼👇🏼👇🏼👇🏼\n👉🏼              👈🏼\n👉🏼              👈🏼\n👉🏼              👈🏼\n👆🏼👆🏼👆🏼👆🏼👆🏼",
        f"👇🏻👇🏻👇🏻\n{name}\n👆🏻👆🏻👆🏻",
        f"👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿\n👉🏿👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👈🏿\n👉🏿👉🏾👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👇🏼👇🏼👇🏼👇🏼👇🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👉🏼👇🏻👇🏻👇🏻👈🏼👈🏽👈🏾👈🏿\n👉🏿  {name}  👈🏿\n👉🏿👉🏾👉🏽👉🏼👆🏻👆🏻👆🏻👈🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👆🏼👆🏼👆🏼👆🏼👆🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽👈🏾👈🏿\n👉🏿👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👈🏿\n👉🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👈🏿",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 6])


@bot.on(hell_cmd(pattern="phub$", outgoing=True))
@bot.on(sudo_cmd(pattern="phub$", allow_sudo=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    await eor(event, "phub")

    animation_chars = [
        "P_",
        "PO_",
        "POR_",
        "PORN_",
        "PORNH_",
        "PORNHU_",
        "PORNHUB_",
        "PORNHUB",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])


@bot.on(hell_cmd(pattern=r"amore$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"amore$", allow_sudo=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    await eor(event, "amore")

    animation_chars = [
        "A_",
        "AM_",
        "AMO_",
        "AMOR_",
        "AMORE_",
        "AMORE❤_",
        ".-.",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])


@bot.on(hell_cmd(pattern=r"sexy$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"sexy$", allow_sudo=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    await eor(event, "Sexy")

    animation_chars = [
        "S_",
        "SE_",
        "SEX_",
        "SEXY_",
        "SEXY👄_",
        "SEXY👄",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])
        
@bot.on(hell_cmd(pattern="istar$", outgoing=True))
@bot.on(sudo_cmd(pattern="istar$", allow_sudo=True))
async def ammastar(hellstar):
  
    if hellstar.fwd_from:
      
        return
      
    animation_interval = 2
    
    animation_ttl = range(0, 11)
    
    await eor(hellstar, "I am A Star")
    
    animation_chars = [
        "I Party like a rockstar",
        "I Look like a movie star",
        "I Play like an all star",
        "I Fuck like a pornstar",
        "Baby I'm a superstar",
    ]
    
    for i in animation_ttl:
      
        await asyncio.sleep(animation_interval)
        
        await hellstar.edit(animation_chars[i % 11])
    
        
@bot.on(hell_cmd(pattern=r"lmoon", outgoing=True))
@bot.on(sudo_cmd(pattern=r"lmoon", allow_sudo=True))
async def test(event):
    if event.fwd_from:
        return
    await eor(event, 
        "🌕🌕🌕🌕🌕🌕🌕🌕\n🌕🌕🌖🌔🌖🌔🌕🌕\n🌕🌕🌗🌔🌖🌓🌕🌕\n🌕🌕🌗🌔🌖🌓🌕🌕\n🌕🌕🌖🌓🌗🌔🌕🌕\n🌕🌕🌗🌑🌑🌓🌕🌕\n🌕🌕🌗👀🌑🌓🌕🌕\n🌕🌕🌘👄🌑🌓🌕🌕\n🌕🌕🌗🌑🌑🌒🌕🌕\n🌕🌖🌑🌑🌑🌑🌔🌕\n🌕🌘🌑🌑🌑🌑🌒🌕\n🌖🌑🌑🌑🌑🌑🌑🌔\n🌕🤜🏻🌑🌑🌑🌑🤛🏻🌕\n🌕🌖🌑🌑🌑🌑🌔🌕\n🌘🌑🌑🌑🌑🌑🌑🌒\n🌕🌕🌕🌕🌕🌕🌕🌕"
    )


@bot.on(hell_cmd(pattern=r"city", outgoing=True))
@bot.on(sudo_cmd(pattern=r"city", allow_sudo=True))
async def test(event):
    if event.fwd_from:
        return
    await eor(event, 
        """☁☁🌞      ☁           ☁
       ☁  ✈         ☁    🚁    ☁    ☁        ☁          ☁     ☁   ☁

🏬🏨🏫🏢🏤🏥🏦🏪🏫
              🌲/     l🚍\🌳👭
           🌳/  🚘 l  🏃 \🌴 👬                       👬  🌴/            l  🚔    \🌲
      🌲/   🚖     l               \
   🌳/🚶           |   🚍         \ 🌴🚴🚴
🌴/                    |                     \🌲"""
    )


@bot.on(hell_cmd(pattern=r"hii", outgoing=True))
@bot.on(sudo_cmd(pattern=r"hii", allow_sudo=True))
async def hi(event):
    if event.fwd_from:
        return
    await eor(event, "🌺✨✨🌺✨🌺🌺🌺\n🌺✨✨🌺✨✨🌺✨\n🌺🌺🌺🌺✨✨🌺✨\n🌺✨✨🌺✨✨🌺✨\n🌺✨✨🌺✨🌺🌺🌺\n☁☁☁☁☁☁☁☁")


@bot.on(hell_cmd(pattern=r"cheer", outgoing=True))
@bot.on(sudo_cmd(pattern=r"cheer", allow_sudo=True))
async def cheer(event):
    if event.fwd_from:
        return
    await eor(event, 
        "💐💐😉😊💐💐\n☕ Cheer Up  🍵\n🍂 ✨ )) ✨  🍂\n🍂┃ (( * ┣┓ 🍂\n🍂┃*💗 ┣┛ 🍂 \n🍂┗━━┛  🍂🎂 For YOU  🍰\n💐💐😌😚💐💐"
    )


@bot.on(hell_cmd(pattern=r"getwell", outgoing=True))
@bot.on(sudo_cmd(pattern=r"getwell", allow_sudo=True))
async def getwell(event):
    if event.fwd_from:
        return
    await eor(event, "🌹🌹🌹🌹🌹🌹🌹🌹 \n🌹😷😢😓😷😢💨🌹\n🌹💝💉🍵💊💐💝🌹\n🌹 GetBetter Soon! 🌹\n🌹🌹🌹🌹🌹🌹🌹🌹")

@bot.on(hell_cmd(pattern="switch$", outgoing=True))
@bot.on(sudo_cmd(pattern="switch$", allow_sudo=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 11)

  #  input_str = event.pattern_match.group(1)

  #  if input_str == "switch":

    await eor(event, "Switch")

    animation_chars = [
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n[👉](https://t.me/ForGo10God)⬜⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬛[👉](https://t.me/ForGo10God)⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬜⬜⬜⬜⬜⬜\n⬜[👆](https://t.me/ForGo10God)⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜[👆](https://t.me/ForGo10God)⬜⬜⬜⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬛[👉](https://t.me/ForGo10God)⬜⬜⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜[🔲](https://github.com/The-HellBot/HellBot)\n⬜⬛⬛[👉](https://t.me/ForGo10God)⬜⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜🔲\n⬜⬛⬛⬛[👉](https://t.me/ForGo10God)⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜[👆](https://t.me/ForGo10God)⬜🔲\n⬜⬛⬛⬛⬛⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬛[👉](https://t.me/ForGo10God)🔲\n⬜⬛⬛⬛⬛⬜⬜\n⬜⬛⬜⬜⬜⬜⬜\n⬛⬛⬜⬜⬜⬜⬜",
         "⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛🔳\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])


@bot.on(hell_cmd(pattern=r"sprinkle", outgoing=True))
@bot.on(sudo_cmd(pattern=r"sprinkle", allow_sudo=True))
async def sprinkle(event):
    if event.fwd_from:
        return
    await eor(event, 
        "✨.•*¨*.¸.•*¨*.¸¸.•*¨*• ƸӜƷ\n🌸🌺🌸🌺🌸🌺🌸🌺\n Sprinkled with love❤\n🌷🌻🌷🌻🌷🌻🌷🌻\n ¨*.¸.•*¨*. ¸.•*¨*.¸¸.•*¨`*•.✨\n🌹🍀🌹🍀🌹🍀🌹🍀"
    )
    

@bot.on(hell_cmd(pattern=r"f", outgoing=True))
@bot.on(sudo_cmd(pattern=r"f", allow_sudo=True))
async def payf(event):
    if event.fwd_from:
        return
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await eor(event, pay)



CmdHelp("animations").add_command(
  'boxs', None, 'Use and see'
).add_command(
  'rain', None, 'Use and see'
).add_command(
  'deploy', None, 'Use and see'
).add_command(
  'dump', None, 'Use and see'
).add_command(
  'fleaveme', None, 'Use and see'
).add_command(
  'loveu', None, 'Use and see'
).add_command(
  'plane', None, 'Use and see'
).add_command(
  'police', None, 'Use and see'
).add_command(
  'jio', None, 'Use and see'
).add_command(
  'solarsystem', None, 'Use and see'
).add_command(
  'degi', None, 'Use and see'
).add_command(
  'nehi', None, 'Use and see'
).add_command(
  'hack', None, 'Im a hacker bitch'
).add_command(
  'hnd', '<your text>', 'A handy animation with the text,'
).add_command(
  'owner', None, 'Use and see'
).add_command(
  'padmin', None, 'Prank promote a user'
).add_command(
  "phub", None, "Animated PORNHUB Typing"
).add_command(
  "amore", None, "Animated AMORE Typing"
).add_command(
  "sexy", None, "Animated SEXY Typing"
).add_command(
  "unoob", None, "Animated text calling them noob🚶"
).add_command(
  "menoob", None, "Animated text claiming you noob"
).add_command(
  "uproo", None, "Animated text claiming you to be proooo"
).add_command(
  "mepro", None, "Animated text calling them proo Af!!"
).add_command(
  "sprinkle", None, "Use and see"
).add_command(
  "getwell", None, "Use and see"
).add_command(
  "cheer", None, "Use and see"
).add_command(
  "hii", None, "Use and see"
).add_command(
  "city", None, "Use and see"
).add_command(
  "lmoon", None, "Use and see"
).add_command(
  "istar", None, "I am a Superstar⚡✨"
).add_command(
  "switch", None, "Click on the switch to reveal the price✨"
).add_command(
  "thanos", None, "A poem on Thanos... Maybe🤐"
).add_command(
  "tp", None, "Use and see"
).add_command(
  "f", "<text>", "Prints the given text in 'F' format"
).add_command(
  "wahack", None, "Whatsapp Hack animation"
).add()
