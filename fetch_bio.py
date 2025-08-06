import requests

def fetch_character_info(name):
    try:
        # Step 1: Search characters
        search_url = f"https://api.jikan.moe/v4/characters?q={name}&limit=5"
        response = requests.get(search_url)
        data = response.json()

        if "data" not in data or not data["data"]:
            return {"error": "Character not found!"}

        for candidate in data["data"]:
            mal_id = candidate["mal_id"]
            full_url = f"https://api.jikan.moe/v4/characters/{mal_id}/full"
            full_response = requests.get(full_url)
            full_data = full_response.json()

            if "data" not in full_data:
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
                    "anime": anime_list
                }

        # If none of the top results had anime info
        fallback = data["data"][0]
        return {
            "name": fallback.get("name"),
            "image_url": fallback.get("images", {}).get("jpg", {}).get("image_url"),
            "about": fallback.get("about", "No bio available."),
            "anime": ["No known anime."]
        }

    except Exception as e:
        return {"error": str(e)}
