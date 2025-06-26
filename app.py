import streamlit as st
from PIL import Image
from datetime import datetime
import os
from recognizer import recognize_character
from fetch_bio import fetch_character_info
from streaming_info import get_streaming_links
from character_gallery import get_character_images, get_google_image_search

# Setup
os.makedirs("training_data", exist_ok=True)
st.set_page_config(
    page_title="Anime Character Identifier",
    page_icon="🎌",
    layout="centered"
)

# Sidebar Theme Toggle
st.sidebar.title("🛠️ Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"], index=0)
if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #f63366;'>🎌 Anime Character Identifier</h1>", unsafe_allow_html=True)
st.markdown("---")

# Upload
uploaded_file = st.file_uploader("📄 Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # Image and recognition
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="📷 Uploaded Image", width=180)

    with col2:
        character_name = recognize_character(image)
        character_name = character_name.split("(")[0].strip()
        st.markdown("#### 🔍 Recognized Character")
        st.success(f"`{character_name}`")

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

        character_name = st.text_input("📌 Proceed with character:", value=character_name)

    st.markdown("---")

    if st.button("📄 Get Character Info"):
        with st.spinner("🔎 Fetching character details..."):
            result = fetch_character_info(character_name)

            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.image(result["image_url"], width=180)
                st.markdown(f"### 👤 {result['name']}")

                with st.expander("📟 About"):
                    st.markdown(result["about"] or "_No bio available._")

                with st.expander("🎮 Anime Appearances"):
                    anime_titles = result["anime"] or ["No known anime."]
                    st.markdown("• " + "<br>• ".join(anime_titles), unsafe_allow_html=True)

                gallery = get_character_images(character_name)
                st.markdown("### 🖼️ Character Gallery")
                if "error" in gallery:
                    st.info("No additional images available.")
                    if "google_search" in gallery:
                        st.markdown(f"🔎 [Search on Google Images]({gallery['google_search']})")
                else:
                    cols = st.columns(min(len(gallery["images"]), 5))
                    for i, img_url in enumerate(gallery["images"]):
                        with cols[i % 5]:
                            st.image(img_url, width=100)

                st.markdown("### 📺 Where to Watch")
                anime_title = anime_titles[0] if anime_titles and anime_titles[0] != "No known anime." else character_name
                streaming = get_streaming_links(anime_title)

                if "error" in streaming:
                    st.info("ℹ️ Streaming info not available.")
                else:
                    for site, url in streaming["links"].items():
                        st.markdown(f"- 🌐 [{site}]({url})")

                st.balloons()
else:
    st.info("👆 Upload an anime image to get started!")

# Footer
st.markdown("""
---
<center style='color: gray;'>Built with ❤️ by Team 18 | Powered by Jikan & Anilist APIs</center>
""", unsafe_allow_html=True)
