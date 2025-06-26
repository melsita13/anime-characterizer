import streamlit as st
from PIL import Image
from datetime import datetime
import os
from recognizer import recognize_characters
from fetch_bio import fetch_character_info
from streaming_info import get_streaming_links
from character_gallery import get_character_images, get_google_image_search
import re

# Setup
os.makedirs("training_data", exist_ok=True)
st.set_page_config(
    page_title="Anime Character Identifier", page_icon="🎌", layout="centered"
)

# Title
st.markdown(
    "<h1 style='text-align: center; color: #f63366;'>🎌 Anime Character Identifier</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Upload
uploaded_file = st.file_uploader(
    "📤 Upload an anime character image", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    # Image and recognition
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="📷 Uploaded Image", width=150)

    with col2:
        character_names = recognize_characters(image, top_k=3)
        character_names = [
            re.sub(r"\s*\(.*?\)", "", name).strip() for name in character_names
        ]

        st.markdown("#### 🔍 Recognized Characters")
        if character_names:
            for name in character_names:
                st.success(f"`{name}`")
        else:
            st.warning("No recognizable characters detected.")

        feedback = st.radio("🤔 Is this correct?", ("Yes", "No"), horizontal=True)
        if feedback == "No":
            corrected_name = st.text_input("✏️ Enter the correct name:")
            if st.button("✅ Submit Correction"):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{corrected_name}_{timestamp}.jpg"
                image.save(os.path.join("training_data", filename))
                with open("labels.csv", "a") as f:
                    f.write(f"{corrected_name},{filename}\n")
                st.success("✅ Correction saved for training!")

        if character_names:
            selected_character = st.selectbox(
                "📌 Proceed with character:", character_names
            )
        else:
            selected_character = st.text_input("📌 Enter character manually:")

    st.markdown("---")

    if st.button("📄 Get Character Info"):
        with st.spinner("🔎 Fetching character details..."):
            result = fetch_character_info(selected_character)

            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.image(result["image_url"], width=180)
                st.markdown(f"### 👤 {result['name']}")

                with st.expander("📟 About"):
                    st.markdown(result["about"] or "_No bio available._")

                with st.expander("🎮 Anime Appearances"):
                    anime_titles = result["anime"] or ["No known anime."]
                    st.markdown(
                        "• " + "<br>• ".join(anime_titles), unsafe_allow_html=True
                    )

                st.markdown("### 🖼️ Character Gallery")
                gallery = get_character_images(selected_character)
                if "error" in gallery:
                    st.info("No additional images available.")
                    if "google_search" in gallery:
                        st.markdown(
                            f"🔎 [Search on Google Images]({gallery['google_search']})"
                        )
                else:
                    num_images = len(gallery["images"])
                    cols = st.columns(min(num_images, 5))
                    for i, img_url in enumerate(gallery["images"]):
                        with cols[i % len(cols)]:
                            st.markdown(
                                f"""
                                <div style='width: 130px; height: 180px; overflow: hidden; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;'>
                                    <img src="{img_url}" style='width: 100%; height: 100%; object-fit: cover;' />
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                st.markdown("### 📺 Where to Watch")
                anime_title = (
                    anime_titles[0]
                    if anime_titles and anime_titles[0] != "No known anime."
                    else selected_character
                )
                streaming = get_streaming_links(anime_title)

                if "error" in streaming:
                    st.info("ℹ️ Streaming info not available.")
                else:
                    for site, url in streaming["links"].items():
                        st.markdown(
                            f"""
                            <a href="{url}" target="_blank" style="
                                display: inline-block;
                                color: #1E90FF;
                                text-decoration: none;
                                font-weight: 500;
                                margin: 4px 0;
                            ">
                                🌐 {site}
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )

                st.success("✅ Done! All character info loaded.")


else:
    st.info("👆 Upload an anime image to get started!")

# Footer
st.markdown(
    """
---
<center style='color: gray;'>Built with ❤️ by Team 18 | Powered by Jikan & Anilist APIs</center>
""",
    unsafe_allow_html=True,
)
