import requests
import urllib.parse

def get_character_images(character_name):
    # Avoid fallback names or unknown results
    if "Related Character" in character_name or "Top Tags" in character_name or "Unknown" in character_name:
        return {
            "error": "Name too generic for Anilist.",
            "google_search": get_google_image_search(character_name)
        }

    # Strip anything after '(' e.g., "Rem (Re:Zero)" → "Rem"
    character_name = character_name.split("(")[0].strip()

    print(f"[DEBUG] Searching for character: {character_name}")

    query = """
    query ($search: String) {
      Character(search: $search) {
        id
        name {
          full
        }
        image {
          large
          medium
        }
        media(perPage: 5) {
          nodes {
            title {
              romaji
            }
            coverImage {
              large
            }
          }
        }
      }
    }
    """

    variables = {"search": character_name}
    url = "https://graphql.anilist.co"

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        data = response.json()

        print("=== Raw Anilist Response ===")
        print(data)

        if "data" not in data or not data["data"]["Character"]:
            return {
                "error": "No character images found.",
                "google_search": get_google_image_search(character_name)
            }

        character = data["data"]["Character"]
        image_list = []

        # Add profile image
        if character.get("image") and character["image"].get("large"):
            image_list.append(character["image"]["large"])

        # Add cover images from media
        for media in character["media"]["nodes"]:
            cover = media.get("coverImage", {}).get("large")
            if cover and cover not in image_list:
                image_list.append(cover)

        print("[INFO] Images found:", image_list)

        return {"images": image_list[:5]}

    except Exception as e:
        print("[ERROR]", e)
        return {
            "error": str(e),
            "google_search": get_google_image_search(character_name)
        }


def get_google_image_search(character_name):
    base = "https://www.google.com/search?tbm=isch&q="
    query = urllib.parse.quote(f"{character_name} anime")
    return f"{base}{query}"