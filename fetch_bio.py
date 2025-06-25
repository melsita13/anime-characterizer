import requests

def fetch_character_info(name):
    try:
        url = f"https://api.jikan.moe/v4/characters?q={name}&limit=10"
        response = requests.get(url)
        data = response.json()

        if "data" not in data or not data["data"]:
            return {"error": "Character not found!"}

        for char in data["data"]:
            anime_list = char.get("anime", [])
            if anime_list:
                return {
                    "name": char.get("name"),
                    "image_url": char.get("images", {}).get("jpg", {}).get("image_url"),
                    "about": char.get("about", "No bio available."),
                    "anime": [entry["anime"]["title"] for entry in anime_list]
                }

        # If none have anime appearances, return the first as fallback
        fallback = data["data"][0]
        return {
            "name": fallback.get("name"),
            "image_url": fallback.get("images", {}).get("jpg", {}).get("image_url"),
            "about": fallback.get("about", "No bio available."),
            "anime": ["No known anime."]
        }

    except Exception as e:
        return {"error": str(e)}