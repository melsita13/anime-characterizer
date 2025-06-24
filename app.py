import streamlit as st
from PIL import Image
from recognizer import recognize_character
from fetch_bio import fetch_character_info
from related_characters import get_related_characters
from streaming_info import get_streaming_links
from character_gallery import get_character_images
from character_gallery import get_google_image_search

st.title("🎌 Anime Character Identifier")

uploaded_file = st.file_uploader("Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=150)

    # Step 1: Detect character
    character_name = recognize_character(image)
    character_name = character_name.split("(")[0].strip()
    character_name = st.text_input("Detected Character:", value=character_name)

    if character_name and character_name != "Unknown Character":
        st.subheader("Recognized Character")

        if st.button("Get character info"):
            with st.spinner("Fetching character details..."):
                # Step 2: Fetch character bio
                result = fetch_character_info(character_name)

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.image(result["image_url"], width=200)
                    # Step 2.5: Show gallery images of this character
                    gallery = get_character_images(character_name)
                    st.markdown("### 🖼️ More Images")
                    if "error" in gallery:
                        st.info("No additional images available.")
                        if "google_search" in gallery:
                            st.markdown(f"🔎 [Try Google Image Search]({gallery['google_search']})")
                    else:
                        img_cols = st.columns(len(gallery["images"]))
                        for i, img_url in enumerate(gallery["images"]):
                            with img_cols[i]:
                                st.image(img_url, width=120)


                    st.markdown(f"### {result['name']}")
                    st.markdown("**About:**")
                    st.markdown(result["about"] or "No bio available.")
                    st.markdown("**Anime Appearances:**")
                    st.markdown(", ".join(result["anime"]) or "No data.")

                    # Step 3: Fetch related characters
                    related = get_related_characters(character_name)
                    if "error" in related:
                        st.warning(
                            f"Could not fetch related characters: {related['error']}"
                        )
                        anime_title = "Unknown Anime"
                    else:
                        anime_title = related.get("anime_title", "Unknown Anime")
                        st.markdown(f"### Related Characters from *{anime_title}*")
                        cols = st.columns(5)
                        for i, char in enumerate(
                            related.get("related_characters", [])[:5]
                        ):
                            with cols[i]:
                                st.image(char["image"], width=100)
                                st.caption(f"{char['name']} ({char['role']})")

                    # Step 4: Fetch streaming info
                    streaming = get_streaming_links(anime_title)
                    st.markdown("### 📺 Where to Watch")
                    if "error" in streaming:
                        st.info("Streaming info not available.")
                    else:
                        for site, url in streaming["links"].items():
                            st.markdown(f"- [{site}]({url})")
    else:
        st.warning("Please upload a clear anime character image.")
