import requests

def get_character_images(character_name):
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

        if "data" not in data or not data["data"]["Character"]:
            return {"error": "No character images found."}

        character = data["data"]["Character"]
        image_list = []

        # Add profile image
        if character["image"]:
            image_list.append(character["image"]["large"])

        # Add media cover images
        for media in character["media"]["nodes"]:
            cover = media.get("coverImage", {}).get("large")
            if cover and cover not in image_list:
                image_list.append(cover)

        return {"images": image_list[:5]}  # Limit to 5 images

    except Exception as e:
        return {"error": str(e)}