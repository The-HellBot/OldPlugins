import os

from HellConfig import Config
from imdb import IMDb
from justwatch import JustWatch

# ======== IMDB Part =========#
imdb = IMDb()
moviepath = os.path.join(os.getcwd(), "temp", "moviethumb.jpg")

# Get all casts
async def get_casts(cast, movie):
    _cast = ""
    if cast in list(movie.keys()):
        i = 0
        for j in movie[cast]:
            if i < 1:
                _cast += str(j)
            elif i < 5:
                _cast += ", " + str(j)
            else:
                break
            i += 1
    else:
        _cast += "No Data"
    return _cast


# Get all movies
async def get_movies(movie):
    result = ""
    if "box office" in movie.keys():
        for i in movie["box office"].keys():
            result += f"\n<b>   • {i}:</b> <code>{movie['box office'][i]}</code>"
    else:
        result = "<code>No Data</code>"
    return result


mov_titles = [
    "long imdb title",
    "long imdb canonical title",
    "smart long imdb canonical title",
    "smart canonical title",
    "canonical title",
    "localized title",
]

# ======== IMDB ENDS ==========#

# ======== JUST WATCH PART ==========#
# Get streaming sites details
def get_stream_data(query):
    stream_data = {}
    try:
        country = Config.WATCH_COUNTRY
    except Exception:
        country = "IN"
    just_watch = JustWatch(country=country)
    results = just_watch.search_for_item(query=query)
    movie = results["items"][0]
    stream_data["title"] = movie["title"]
    stream_data["movie_thumb"] = (
        "https://images.justwatch.com"
        + movie["poster"].replace("{profile}", "")
        + "s592"
    )
    stream_data["release_year"] = movie["original_release_year"]
    try:
        print(movie["cinema_release_date"])
        stream_data["release_date"] = movie["cinema_release_date"]
    except KeyError:
        try:
            stream_data["release_date"] = movie["localized_release_date"]
        except KeyError:
            stream_data["release_date"] = None

    stream_data["type"] = movie["object_type"]

    available_streams = {}
    for provider in movie["offers"]:
        provider_ = get_provider(provider["urls"]["standard_web"])
        available_streams[provider_] = provider["urls"]["standard_web"]

    stream_data["providers"] = available_streams

    scoring = {}
    for scorer in movie["scoring"]:
        if scorer["provider_type"] == "tmdb:score":
            scoring["tmdb"] = scorer["value"]

        if scorer["provider_type"] == "imdb:score":
            scoring["imdb"] = scorer["value"]
    stream_data["score"] = scoring
    return stream_data


# Pretty format for google play movies
def pretty(name):
    if name == "play":
        name = "Google Play Movies"
    return name[0].upper() + name[1:]


# Stream providers name.
def get_provider(url):
    url = url.replace("https://www.", "")
    url = url.replace("https://", "")
    url = url.replace("http://www.", "")
    url = url.replace("http://", "")
    url = url.split(".")[0]
    return url


# =========== JUST WATCH ENDS =============#
