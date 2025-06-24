import requests

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
    url = "https://graphql.anilist.co"

    try:
        response = requests.post(url, json={"query":query, "variables":variables})
        data = response.json()

        if "data" not in data or not data["data"]["media"]:
            return {"error": "No streaming data found."}
        
        episodes = data["data"]["media"]["streamingEpisodes"]
        if not episodes:
            return {"error": "No streaming episodes availbale"}
        
        links_by_site = {}
        for ep in episodes:
            site = ep["site"]
            if site not in links_by_site:
                links_by_site[site] = ep["url"]
                
        return {"links": links_by_site}
    
    except Exception as e:
        return {"error":str(e)}