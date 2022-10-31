import os

from bs4 import BeautifulSoup
from pySmartDL import SmartDL
from TelethonHell.plugins import *

logo = "https://te.legra.ph/file/2c546060b20dfd7c1ff2d.jpg"


@hell_cmd(pattern="imdb(?:\s|$)([\s\S]*)")
async def _(event):
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(event, "Nothing given to search.")
    hell = await eor(event, f"Searching `{lists[1]}` in IMDb...")
    try:
        # IB: catuserbot.
        movies = imdb.search_movie(lists[1])
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
        paste = await telegraph_paste(f"IMDb Movie Result for “ {lists[1]} ”", telegraph_)
        omk = f"{omk_}\n\n<u><b><a href='{paste}'>📌 Get more details here.</a></b></u>"
        if os.path.exists(moviepath):
            await event.client.send_file(
                event.chat_id,
                moviepath,
                caption=omk,
                reply_to=reply,
                parse_mode="HTML",
            )
            os.remove(moviepath)
            return await hell.delete()
        await hell.edit(
            omk,
            link_preview=False,
            parse_mode="HTML",
        )
    except IndexError:
        await parse_error(hell, f"__No movie found with name__ `{lists[1]}`", False)
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="watch(?:\s|$)([\s\S]*)")
async def _(event):
    query = event.pattern_match.group(1)
    hell = await eor(event, "Finding Sites...")
    streams = get_stream_data(query)
    title = streams["title"]

    thumb_link = streams["movie_thumb"]
    title_img = None
    if thumb_link:
        banner = requests.get(thumb_link)
        open("hellbot_watch.jpg", "wb").write(banner.content)
        title_img = "hellbot_watch.jpg"

    release_year = streams["release_year"]
    release_date = streams["release_date"]

    scores = streams["score"]
    try:
        imdb_score = scores["imdb"]
    except KeyError:
        imdb_score = None

    try:
        tmdb_score = scores["tmdb"]
    except KeyError:
        tmdb_score = None

    stream_providers = streams["providers"]
    if release_date is None:
        release_date = release_year

    output_ = f"**Movie:**\n`{title}`\n**Release Date:**\n`{release_date}`"
    if imdb_score:
        output_ = output_ + f"\n**IMDB: **{imdb_score}"
    if tmdb_score:
        output_ = output_ + f"\n**TMDB: **{tmdb_score}"

    output_ = output_ + "\n\n**Available on:**\n"
    for provider, link in stream_providers.items():
        if "sonyliv" in link:
            link = link.replace(" ", "%20")
        output_ += f"[{pretty(provider)}]({link})\n"

    await event.client.send_file(
        event.chat_id,
        caption=output_,
        file=title_img,
        force_document=False,
        allow_cache=False,
        silent=True,
    )
    await hell.delete()


CmdHelp("movies").add_command(
    "imdb", "<movie name>", "Searches for given movie on IMDb database and returns the details.", "imdb The Shawshank Redemption"
).add_command(
    "watch", "<movie name>", "Searches for all the available sites for watching that movie or series", "watch Godfather"
).add_info(
    "All about movies."
).add_warning(
    "✅ Harmless Module."
).add()
