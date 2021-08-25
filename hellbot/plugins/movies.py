import os
from pySmartDL import SmartDL
from bs4 import BeautifulSoup

from . import *

logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"

@bot.on(hell_cmd(pattern="imdb ?(.*)"))
@bot.on(sudo_cmd(pattern="imdb ?(.*)", allow_sudo=True))
async def _(event):
    reply_to = await reply_id(event)
    hel_ = await eor(event, "`Processing ...`")
    try:
        hell = event.pattern_match.group(1)
        await hel_.edit("__Searching for__ `{}`".format(hell))
        # Credits to catuserbot.
        # Ported to Hellbot and beautifications by @ForGo10God.
        movies = imdb.search_movie(hell)
        movieid = movies[0].movieID
        movie = imdb.get_movie(movieid)
        moviekeys = list(movie.keys())
        for i in mov_titles:
            if i in moviekeys:
                mov_title = movie[i]
                break
        for j in reversed(mov_titles):
            if j in moviekeys:
                mov_ltitle = movie[j]
                break
        mov_runtime = movie["runtimes"][0] + " min" if "runtimes" in movie else ""
        if "original air date" in moviekeys:
            mov_airdate = movie["original air date"]
        elif "year" in moviekeys:
            mov_airdate = movie["year"]
        else:
            mov_airdate = ""
        mov_genres = ", ".join(movie["genres"]) if "genres" in moviekeys else "No Data"
        mov_rating = str(movie["rating"]) if "rating" in moviekeys else "No Data"
        mov_rating += (
            " (by " + str(movie["votes"]) + ")"
            if "votes" in moviekeys and "rating" in moviekeys
            else ""
        )
        mov_countries = (
            ", ".join(movie["countries"]) if "countries" in moviekeys else "No Data"
        )
        mov_languages = (
            ", ".join(movie["languages"]) if "languages" in moviekeys else "No Data"
        )
        mov_plot = (
            str(movie["plot outline"]) if "plot outline" in moviekeys else "No Data"
        )
        mov_director = await get_casts("director", movie)
        mov_composers = await get_casts("composers", movie)
        mov_writer = await get_casts("writer", movie)
        mov_cast = await get_casts("cast", movie)
        mov_box = await get_movies(movie)
        resulttext = f"""
<u><b>✘ Title :</b></u> <code>{mov_title}</code>\n
<u><b>✘ Imdb Url :</b></u> <a href='https://www.imdb.com/title/tt{movieid}'>{mov_ltitle}</a>\n
<u><b>✘ Info :</b></u> <code>{mov_runtime} | {mov_airdate}</code>\n
<b><u>✘ Genres :</u></b> <code>{mov_genres}</code>\n
<u><b>✘ Rating :</b></u> <code>{mov_rating}</code>\n
<u><b>✘ Country :</b></u> <code>{mov_countries}</code>\n
<u><b>✘ Language :</b></u> <code>{mov_languages}</code>\n
<u><b>✘ Director :</b></u> <code>{mov_director}</code>\n
<u><b>✘ Music Director :</b></u> <code>{mov_composers}</code>\n
<u><b>✘ Writer :</b></u> <code>{mov_writer}</code>\n
<u><b>✘ Stars :</b></u> <code>{mov_cast}</code>\n
<u><b>✘ Box Office :</b></u> {mov_box}\n
<u><b>✘ Story Outline :</b></u> <i>{mov_plot}</i>"""

        omk_ = f"""
<b>Title :</b> <code>{mov_title}</code>
<b>Imdb Url :</b> <a href='https://www.imdb.com/title/tt{movieid}'>{mov_ltitle}</a>
<b>Info :</b> <code>{mov_runtime} | {mov_airdate}</code>
<b>Genres :</b> <code>{mov_genres}</code>
<b>Rating :</b> <code>{mov_rating}</code>
<b>Country :</b> <code>{mov_countries}</code>
<b>Language :</b> <code>{mov_languages}</code>
<b>Director :</b> <code>{mov_director}</code>"""
        if "full-size cover url" in moviekeys:
            imageurl = movie["full-size cover url"]
        else:
            imageurl = None
        soup = BeautifulSoup(resulttext, features="html.parser")
        rtext = soup.get_text()
        if len(rtext) > 1024:
            extralimit = len(rtext) - 1024
            climit = len(resulttext) - extralimit - 20
            resulttext = resulttext[:climit] + "...........</i>"
        if imageurl:
            downloader = SmartDL(imageurl, moviepath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        telegraph_ = f"<img src='{imageurl}'/> \n{resulttext} \n<img src='{logo}'/>"
        paste = await telegraph_paste(f"IMDb Movie Result for “ {hell} ”", telegraph_)
        omk = f"{omk_}\n\n<u><b><a href='{paste}'>📌 Get more details here.</a></b></u>"
        if os.path.exists(moviepath):
            await event.client.send_file(
                event.chat_id,
                moviepath,
                caption=omk,
                reply_to=reply_to,
                parse_mode="HTML",
            )
            os.remove(moviepath)
            return await hel_.delete()
        await hel_.edit(
            omk,
            link_preview=False,
            parse_mode="HTML",
        )
    except IndexError:
        await hel_.edit(f"__No movie found with name {hell}.__")
    except Exception as e:
        await hel_.edit(f"**Error:**\n__{e}__")


CmdHelp("movies").add_command(
  "imdb", "<movie name>", "Searches for given movie on IMDb database and returns the details.", "imdb The Shawshank Redemption"
).add_command(
  "watch", "<movie name>", "#Soon", "watch Godfather"
).add_info(
  "All about movies."
).add_warning(
  "✅ Harmless Module."
).add()
