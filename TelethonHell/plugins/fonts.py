from TelethonHell.plugins import *

normal_str = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
one = "𝔄 𝔅 ℭ 𝔇 𝔈 𝔉 𝔊 ℌ ℑ 𝔍 𝔎 𝔏 𝔐 𝔑 𝔒 𝔓 𝔔 ℜ 𝔖 𝔗 𝔘 𝔙 𝔚 𝔛 𝔜 ℨ"
two = "𝕬 𝕭 𝕮 𝕯 𝕰 𝕱 𝕲 𝕳 𝕴 𝕵 𝕶 𝕷 𝕸 𝕹 𝕺 𝕻 𝕼 𝕽 𝕾 𝕿 𝖀 𝖁 𝖂 𝖃 𝖄 𝖅"
three = "𝓐 𝓑 𝓒 𝓓 𝓔 𝓕 𝓖 𝓗 𝓘 𝓙 𝓚 𝓛 𝓜 𝓝 𝓞 𝓟 𝓠 𝓡 𝓢 𝓣 𝓤 𝓥 𝓦 𝓧 𝓨 𝓩"
four = "𝒜 𝐵 𝒞 𝒟 𝐸 𝐹 𝒢 𝐻 𝐼 𝒥 𝒦 𝐿 𝑀 𝒩 𝒪 𝒫 𝒬 𝑅 𝒮 𝒯 𝒰 𝒱 𝒲 𝒳 𝒴 𝒵"
five = "𝔸 𝔹 ℂ 𝔻 𝔼 𝔽 𝔾 ℍ 𝕀 𝕁 𝕂 𝕃 𝕄 ℕ 𝕆 ℙ ℚ ℝ 𝕊 𝕋 𝕌 𝕍 𝕎 𝕏 𝕐 ℤ"
six = "Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ Ｉ Ｊ Ｋ Ｌ Ｍ Ｎ Ｏ Ｐ Ｑ Ｒ Ｓ Ｔ Ｕ Ｖ Ｗ Ｘ Ｙ Ｚ"
seven = "ꪖ ᥇ ᥴ ᦔ ꫀ ᠻ ᧁ ꫝ ꠸ ꠹ ᛕ ꪶ ꪑ ꪀ ꪮ ρ ꪇ ᥅ ᦓ ꪻ ꪊ ꪜ ᭙ ᥊ ꪗ ƺ"
eight = "ᴀ ʙ ᴄ ᴅ ᴇ ꜰ ɢ ʜ ɪ ᴊ ᴋ ʟ ᴍ ɴ ᴏ ᴘ Q ʀ ꜱ ᴛ ᴜ ᴠ ᴡ x ʏ ᴢ"
nine = "Z ⅄ X M Λ ∩ ⊥ S ᴚ Ό Ԁ O N W ˥ ⋊ ſ I H ⅁ Ⅎ Ǝ ᗡ Ɔ ᙠ ∀"
ten = "🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹 🄺 🄻 🄼 🄽 🄾 🄿 🅀 🅁 🅂 🅃 🅄 🅅 🅆 🅇 🅈 🅉"
eleven = "Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ Ⓕ Ⓖ Ⓗ Ⓘ Ⓙ Ⓚ Ⓛ Ⓜ Ⓝ Ⓞ Ⓟ Ⓠ Ⓡ Ⓢ Ⓣ Ⓤ Ⓥ Ⓦ Ⓧ Ⓨ Ⓩ"
twelve = "ค ๒ ς ๔ є Ŧ ﻮ ђ เ ן к ɭ ๓ ภ ๏ ק ợ г ร Շ ย ש ฬ א ץ չ"
thirteen = "ǟ ɮ ƈ ɖ ɛ ʄ ɢ ɦ ɨ ʝ ӄ ʟ ʍ ռ օ ք զ ʀ ֆ ȶ ʊ ʋ ա Ӽ ʏ ʐ"
fourteen = "Ꮧ Ᏸ ፈ Ꮄ Ꮛ Ꭶ Ꮆ Ꮒ Ꭵ Ꮰ Ꮶ Ꮭ Ꮇ Ꮑ Ꭷ Ꭾ Ꭴ Ꮢ Ꮥ Ꮦ Ꮼ Ꮙ Ꮗ ጀ Ꭹ ፚ"
fifteen = "ą ც ƈ ɖ ɛ ʄ ɠ ɧ ı ʝ ƙ Ɩ ɱ ŋ ơ ℘ զ ཞ ʂ ɬ ų ۷ ῳ ҳ ყ ʑ"
sixteen = "ค ๖ ¢ ໓ ē f ງ h i ว k l ๓ ຖ ໐ p ๑ r Ş t น ง ຟ x ฯ ຊ"
seventeen = "𝐀 𝐁 𝐂 𝐃 𝐄 𝐅 𝐆 𝐇 𝐈 𝐉 𝐊 𝐋 𝐌 𝐍 𝐎 𝐏 𝐐 𝐑 𝐒 𝐓 𝐔 𝐕 𝐖 𝐗 𝐘 𝐙"
eighteen = "𝗔 𝗕 𝗖 𝗗 𝗘 𝗙 𝗚 𝗛 𝗜 𝗝 𝗞 𝗟 𝗠 𝗡 𝗢 𝗣 𝗤 𝗥 𝗦 𝗧 𝗨 𝗩 𝗪 𝗫 𝗬 𝗭"
nineteen = "α в ¢ ∂ є ƒ g н ι נ к ℓ м η σ ρ q я ѕ т υ ν ω χ у z"
twenty = "Ä ß Ç Ð È £ G H Ì J K L M ñ Ö þ Q R § † Ú V W × ¥ Z"
twentyone = "₳ ฿ ₵ Đ Ɇ ₣ ₲ Ⱨ ł J ₭ Ⱡ ₥ ₦ Ø ₱ Q Ɽ ₴ ₮ Ʉ V ₩ Ӿ Ɏ Ⱬ"
twentytwo = "卂 乃 匚 ᗪ 乇 千 Ꮆ 卄 丨 ﾌ Ҝ ㄥ 爪 几 ㄖ 卩 Ɋ 尺 丂 ㄒ ㄩ ᐯ 山 乂 ㄚ 乙"
twentythree = "ﾑ 乃 ᄃ り 乇 ｷ ム ん ﾉ ﾌ ズ ﾚ ﾶ 刀 の ｱ ゐ 尺 丂 ｲ ひ √ W ﾒ ﾘ 乙"
twentyfour = "ą ც ƈ ɖ ɛ ʄ ɠ ɧ ı ʝ ƙ Ɩ ɱ ŋ ơ ℘ զ ཞ ʂ ɬ ų ۷ ῳ ҳ ყ ʑ"

@hell_cmd(pattern="font(?:\s|$)([\s\S]*)")
async def font(event):
    hell = await eor(event, "Changing font...")
    flag = event.text[6:]
    rply = await event.get_reply_message()
    if not rply:
        return await eod(hell, "Nothing given to change!")
    old = rply.text
    normie = normal_str.split(" ")
    prev = " ".join(old).upper()
    if flag.isnumeric():
        font_number = int(flag)
        if font_number == 1:
            to_ = one.split(" ")
        elif font_number == 2:
            to_ = two.split(" ")
        elif font_number == 3:
            to_ = three.split(" ")
        elif font_number == 4:
            to_ = four.split(" ")
        elif font_number == 5:
            to_ = five.split(" ")
        elif font_number == 6:
            to_ = six.split(" ")
        elif font_number == 7:
            to_ = seven.split(" ")
        elif font_number == 8:
            to_ = eight.split(" ")
        elif font_number == 9:
            to_ = nine.split(" ")
        elif font_number == 10:
            to_ = ten.split(" ")
        elif font_number == 11:
            to_ = eleven.split(" ")
        elif font_number == 12:
            to_ = twelve.split(" ")
        elif font_number == 13:
            to_ = thirteen.split(" ")
        elif font_number == 14:
            to_ = fourteen.split(" ")
        elif font_number == 15:
            to_ = fifteen.split(" ")
        elif font_number == 16:
            to_ = sixteen.split(" ")
        elif font_number == 17:
            to_ = seventeen.split(" ")
        elif font_number == 18:
            to_ = eighteen.split(" ")
        elif font_number == 19:
            to_ = nineteen.split(" ")
        elif font_number == 20:
            to_ = twenty.split(" ")
        elif font_number == 21:
            to_ = twentyone.split(" ")
        elif font_number == 22:
            to_ = twentytwo.split(" ")
        elif font_number == 23:
            to_ = twentythree.split(" ")
        elif font_number == 24:
            to_ = twentyfour.split(" ")
        else:
            await eod(hell, "Unsupported font!")
            return

        for normal in prev:
            if normal in normie:
                new = to_[normie.index(normal)]
                prev = prev.replace(normal, new)
        await hell.edit(prev)
    else:
        await eod(hell, "Give font numbers only!")


CmdHelp("fonts").add_command(
    "font", "<font number>", "Changes the replied text to the desired font.", "font 7"
).add_extra(
    "📌 Font Numbers", "1 to N (number of available fonts)"
).add_info(
    "Font Changer."
).add_warning(
    "✅ Harmless Module"
).add()
