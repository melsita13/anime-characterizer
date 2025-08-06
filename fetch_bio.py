from utils.api_handler import make_api_request, JIKAN_URL


def fetch_character_info(name):
    """
    Fetch character information from the Jikan API.
    :param name: The name of the character to search for.
    :return: A dictionary containing character details or an error message.
    """
    search_url = f"{JIKAN_URL}/characters"
    search_data = make_api_request(search_url, params={"q": name, "limit": 5})

    if "error" in search_data or "data" not in search_data or not search_data["data"]:
        return {"error": "Character not found!"}

    for candidate in search_data["data"]:
        mal_id = candidate["mal_id"]
        full_url = f"{JIKAN_URL}/characters/{mal_id}/full"
        full_data = make_api_request(full_url)

        if "error" in full_data or "data" not in full_data:
            continue

        char = full_data["data"]
        anime_list = []

        if "animeography" in char:
            anime_list = [entry["anime"]["title"] for entry in char["animeography"]]
        elif "anime" in char:
            anime_list = [entry["anime"]["title"] for entry in char["anime"]]

        if anime_list:
            return {
                "name": char.get("name"),
                "image_url": char.get("images", {}).get("jpg", {}).get("image_url"),
                "about": char.get("about") or "No bio available.",
                "anime": anime_list,
            }

    fallback = search_data["data"][0]
    return {
        "name": fallback.get("name"),
        "image_url": fallback.get("images", {}).get("jpg", {}).get("image_url"),
        "about": fallback.get("about", "No bio available."),
        "anime": ["No known anime."],
    }
