from utils.api_handler import make_api_request, ANILIST_URL


def get_streaming_links(anime_title):
    query = """
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        title {
          romaji
        }
        streamingEpisodes {
          title
          thumbnail
          url
          site
        }
      }
    }
    """
    variables = {"search": anime_title}

    data = make_api_request(
        ANILIST_URL, method="POST", json={"query": query, "variables": variables}
    )

    if "error" in data or "data" not in data or not data["data"]["Media"]:
        return {"error": "No streaming data found."}

    episodes = data["data"]["Media"]["streamingEpisodes"]
    if not episodes:
        return {"error": "No streaming episodes available."}

    links_by_site = {}
    for ep in episodes:
        site = ep["site"]
        if site not in links_by_site:
            links_by_site[site] = ep["url"]

    return {"links": links_by_site}