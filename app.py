import streamlit as st
from PIL import Image
from recognizer import recognize_character
from fetch_bio import fetch_character_info
from related_characters import get_related_characters

st.title("🎌 Anime Character Identifier")

uploaded_file = st.file_uploader("Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=150)

    # Step 1: Detect character
    character_name = recognize_character(image)
    character_name = st.text_input("Detected Character:", value=character_name)

    if character_name and character_name != "Unknown Character":
        st.subheader("Recognized Character")

        if st.button("Get character info"):
            with st.spinner("Fetching character details..."):
                # Step 2: Fetch bio
                result = fetch_character_info(character_name)

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.image(result["image_url"], width=200)
                    st.markdown(f"### {result['name']}")
                    st.markdown("**About:**")
                    st.markdown(result["about"] or "No bio available.")
                    st.markdown("**Anime Appearances:**")
                    st.markdown(", ".join(result["anime"]) or "No data.")

                    # Step 3: Fetch related characters
                    related = get_related_characters(character_name)
                    if "error" in related:
                        st.warning(f"Could not fetch related characters: {related['error']}")
                    else:
                        anime_title = related.get("anime_title", "Unknown Anime")
                        st.markdown(f"### Related Characters from *{anime_title}*")
                        cols = st.columns(5)
                        for i, char in enumerate(related["related_characters"],[])[:5]:
                            with cols[i]:
                                st.image(char["image"], width=100)
                                st.caption(f"{char['name']} ({char['role']})")
    else:
        st.warning("Please upload a clear anime character image.")
