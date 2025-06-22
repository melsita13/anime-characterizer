import requests

def fetch_character_info(name):
    try:
        url = f"https://api.jikan.moe/v4/characters?q={name}&limit=1"
        response = requests.get(url)
        data = response.json()

        if "data" in data and data["data"]:
            char = data["data"][0]
            return {
                "name": char.get("name"),
                "image_url": char.get("images", {}).get("jpg", {}).get("image_url"),
                "about": char.get("about"),
                "anime": [entry["anime"]["title"] for entry in char.get("anime",[])]
            }
        else:
            return {"error": "Character not found!"}
    except Exception as e:
        return {"error": str(e)}