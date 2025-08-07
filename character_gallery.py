import urllib.parse
from utils.name_cleaner import clean_character_name
from utils.api_handler import make_api_request, ANILIST_URL


def get_character_images(character_name):
    """Fetches images of a character from Anilist based on the provided character name."""

    if (
        "Related Character" in character_name
        or "Top Tags" in character_name
        or "Unknown" in character_name
    ):
        return {
            "error": "Name too generic for Anilist.",
            "google_search": get_google_image_search(character_name),
        }

    if not isinstance(character_name, str):
        return {"error": "Invalid character name format.", "google_search": get_google_image_search(character_name)}

    character_name = clean_character_name(character_name)
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

    data = make_api_request(
        ANILIST_URL, method="post", json_data={"query": query, "variables": variables}
    )

    if "error" in data or "data" not in data or not data["data"]["Character"]:
        return {
            "error": "No character images found.",
            "google_search": get_google_image_search(character_name),
        }

    character = data["data"]["Character"]
    image_list = []

    if character.get("image") and character["image"].get("large"):
        image_list.append(character["image"]["large"])

    for media in character["media"]["nodes"]:
        cover = media.get("coverImage", {}).get("large")
        if cover and cover not in image_list:
            image_list.append(cover)

    print("[INFO] Images found:", image_list)

    return {"images": image_list[:5]}


def get_google_image_search(character_name):
    base = "https://www.google.com/search?tbm=isch&q="
    query = urllib.parse.quote(f"{character_name} anime")
    return f"{base}{query}"