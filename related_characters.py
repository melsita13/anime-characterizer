import requests

def get_related_characters(character_name):
    try:
        # Step 1: Get character ID from Jikan
        char_url = f"https://api.jikan.moe/v4/characters?q={character_name}&limit=1"
        char_res = requests.get(char_url).json()

        if not char_res["data"]:
            return {"error": "Character not found"}

        character = char_res["data"][0]
        anime_list = character.get("anime", [])
        if not anime_list:
            return {"error": "No anime found for character"}

        # Step 2: Use the first anime to get its main characters
        anime_id = anime_list[0]["anime"]["mal_id"]
        anime_title = anime_list[0]["anime"]["title"]
        character_url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
        characters_res = requests.get(character_url).json()

        characters = characters_res.get("data", [])[:6]  # top 6 characters
        related = []

        for c in characters:
            if c["character"]["name"] != character_name:
                related.append({
                    "name": c["character"]["name"],
                    "image": c["character"]["images"]["jpg"]["image_url"],
                    "role": c["role"]
                })

        return {
            "anime_title": anime_title,
            "related_characters": related[:5]  # limit to 5
        }

    except Exception as e:
        return {"error": str(e)}