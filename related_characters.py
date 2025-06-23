import requests

def get_related_characters(character_name, fallback_anime=None):
    try:
        # Step 1: Search for character
        char_url = f"https://api.jikan.moe/v4/characters?q={character_name}&limit=5"
        char_res = requests.get(char_url).json()
        candidates = char_res.get("data", [])

        if not candidates:
            return {"error": "Character not found"}

        # Step 2: Try to select the correct character using fallback anime
        selected = None
        if fallback_anime:
            for candidate in candidates:
                for anime_entry in candidate.get("anime", []):
                    if fallback_anime.lower() in anime_entry["anime"]["title"].lower():
                        selected = candidate
                        break
                if selected:
                    break

        # If no match using fallback, pick the first candidate
        if not selected:
            selected = candidates[0]

        anime_list = selected.get("anime", [])
        if not anime_list:
            return {"error": "No anime found for character"}

        anime_id = anime_list[0]["anime"]["mal_id"]
        anime_title = anime_list[0]["anime"]["title"]

        # Step 3: Fetch characters from that anime
        characters_url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
        characters_res = requests.get(characters_url).json()
        all_characters = characters_res.get("data", [])

        related = []
        for char in all_characters:
            if char["character"]["name"] != character_name:
                related.append({
                    "name": char["character"]["name"],
                    "image": char["character"]["images"]["jpg"]["image_url"],
                    "role": char["role"]
                })

        return {
            "anime_title": anime_title,
            "related_characters": related[:5]  # Return top 5
        }

    except Exception as e:
        return {"error": str(e)}