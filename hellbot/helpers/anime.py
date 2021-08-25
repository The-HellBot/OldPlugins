import json
import re
import requests
from bs4 import BeautifulSoup
from .pasters import telegraph_paste


AIR_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    status
    countryOfOrigin
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    siteUrl
    isFavourite
    mediaListEntry {
      status
      id
    }
  }
}
"""


def search_filler(query):
    html = requests.get("https://www.animefillerlist.com/shows").text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", attrs={"class": "Group"})
    index = {}
    for i in div:
        li = i.findAll("li")
        for jk in li:
            yum = jk.a["href"].split("/")[-1]
            cum = jk.text
            index[cum] = yum
    ret = {}
    keys = list(index.keys())
    for i in range(len(keys)):
        if query.lower() in keys[i].lower():
            ret[keys[i]] = index[keys[i]]
    return ret


def parse_filler(filler_id):
    url = "https://www.animefillerlist.com/shows/" + filler_id
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": "Condensed"})
    all_ep = div.find_all("span", attrs={"class": "Episodes"})
    if len(all_ep) == 1:
        ttl_ep = all_ep[0].findAll("a")
        total_ep = []
        mix_ep = None
        filler_ep = None
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": filler_ep,
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 2:
        ttl_ep = all_ep[0].findAll("a")
        fl_ep = all_ep[1].findAll("a")
        total_ep = []
        mix_ep = None
        ac_ep = None
        filler_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 3:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 4:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        al_ep = all_ep[3].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        for aol in al_ep:
            ac_ep.append(aol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ", ".join(ac_ep),
        }
        return dict_


async def callAPI(search_str):
    query = """
    query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    """
    variables = {"search": search_str}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.text


async def formatJSON(outData):
    msg = ""
    jsonData = json.loads(outData)
    res = list(jsonData.keys())
    if "errors" in res:
        msg += f"**Error :** `{jsonData['errors'][0]['message']}`"
        return msg
    else:
        jsonData = jsonData["data"]["Media"]
        idm = jsonData["id"]
        banner = f"https://img.anili.st/media/{idm}"
        banner_ = requests.get(banner)
        open(f"{idm}.jpg", "wb").write(banner_.content)
        title_img = f"{mid}.jpg"
        title = jsonData["title"]["romaji"]
        link = f"https://anilist.co/anime/{jsonData['id']}"
        msg += f"**✘ Anime :** [{title}]({link})"
        msg += f"\n\n**✘ Type :** `{jsonData['format']}`"
        msg += f"\n**✘ Genres :** "
        for g in jsonData["genres"]:
            msg += "`" + g + "`, "
        msg += f"\n**✘ Status :** `{jsonData['status']}`"
        msg += f"\n**✘ Episode :** `{jsonData['episodes']}`"
        msg += f"\n**✘ Year :** `{jsonData['startDate']['year']}`"
        msg += f"\n**✘ Score :** `{jsonData['averageScore']}`"
        msg += f"\n**✘ Duration :** `{jsonData['duration']} min/ep`"
        descr = f"{jsonData['description']}"
        paste = await telegraph_paste(f"Description For “ {title} ”", descr)
        msg += f"\n**✘ Description :** [Read Here]({paste})"
        return title_img, msg


def cflag(country):
    if country == "JP":
        return "\U0001F1EF\U0001F1F5"
    if country == "CN":
        return "\U0001F1E8\U0001F1F3"
    if country == "KR":
        return "\U0001F1F0\U0001F1F7"
    if country == "TW":
        return "\U0001F1F9\U0001F1FC"


def pos_no(no):
    ep_ = list(str(no))
    x = ep_.pop()
    if ep_ != [] and ep_.pop()=='1':
        return 'th'
    th = "st" if x == "1" else "nd" if x == "2" else "rd" if x == "3" else "th"
    return th


def make_it_rw(time_stamp):
    seconds, milliseconds = divmod(int(time_stamp), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]


async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    return requests.post(url, json={"query": query, "variables": vars_}).json()


async def get_airing(vars_):
    result = await return_json_senpai(AIR_QUERY, vars_)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]
    data = result["data"]["Media"]
    mid = data.get("id")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    status = data.get("status")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)
    banner = f"https://img.anili.st/media/{mid}"
    banner_ = requests.get(banner)
    open(f"{mid}.jpg", "wb").write(banner_.content)
    coverImg = f"{mid}.jpg"
    in_ls = False
    in_ls_id = ""
    user_data = ""
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        episode = data["nextAiringEpisode"]["episode"]
        th = pos_no(episode)
        air_on = make_it_rw(nextAir*1000)
    title_ = english or romaji
    out = f"[{c_flag}] **{title_}**"
    out += f"\n**✪ ID :** `{mid}`"
    out += f"\n**✪ Status :** `{status}`\n"
    if air_on:
        out += f"\n**✪ Airing Episode** `{episode}{th}` **in** `{air_on}`"
    site = data["siteUrl"]
    return [coverImg, out], site, [mid, in_ls, in_ls_id]
