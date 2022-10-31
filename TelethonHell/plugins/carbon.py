from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from TelethonHell.plugins import *


@hell_cmd(pattern="carbon(?:\s|$)([\s\S]*)")
async def carbon(event):
    hell = await eor(event, "__Making carbon ... 25%__")
    _, _, hell_mention = await client_id(event)
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if reply:
        _text = reply.message
    else:
        if len(lists) < 2:
            return await parse_error(hell, "Nothing given to make carbon.")
        _text = lists[1]
    text = deEmojify(_text)
    code = quote_plus(text)

    await hell.edit("__Making carbon ... 50%__")
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": "./"})
    chrome_options.binary_location = Config.CHROME_BIN
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(f"https://carbon.now.sh/?l=auto&code={code}")

    await hell.edit("__Making carbon ... 75%__")
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": "./"},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()

    await hell.edit("__Making carbon ... 100%__")
    await event.client.send_file(
        event.chat_id,
        "./carbon.png",
        caption=f"**Carbonized by:** {hell_mention}",
        force_document=True,
        reply_to=reply,
    )
    os.remove("./carbon.png")
    driver.quit()
    await hell.delete()


@hell_cmd(pattern="kargb(?:\s|$)([\s\S]*)")
async def kargb(event):
    hell = await eor(event, "__Making carbon ...  25%__")
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    theme = random.choice(carbon_theme)
    _, _, hell_mention = await client_id(event)
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if reply:
        _text = reply.message
    else:
        if len(lists) < 2:
            return await parse_error(hell, "Nothing given to make carbon.")
        _text = lists[1]
    text = deEmojify(_text)
    code = quote_plus(text)

    await hell.edit("__Making carbon ... 50%__")
    url = f"https://carbon.now.sh/?bg=rgba({R}%2C{G}%2C{B}%2C1)&t={theme}&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}"
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": "./"})
    chrome_options.binary_location = Config.CHROME_BIN
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)

    await hell.edit("__Making carbon ... 75%__")
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": "./"},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()

    await hell.edit("__Making carbon ... 100%__")
    await event.client.send_file(
        event.chat_id,
        "./carbon.png",
        caption=f"**Carbonized by:** {hell_mention}",
        force_document=True,
        reply_to=reply,
    )
    os.remove("./carbon.png")
    await hell.delete()


CmdHelp("carbon").add_command(
    "carbon", "<your text>", "Carbonize your text. (Fixed style)"
).add_command(
    "kargb", "<your text>", "Carbonize your text.(random style)"
).add_info(
    "Carbonizer"
).add_warning(
    "✅ Harmless Module."
).add()
