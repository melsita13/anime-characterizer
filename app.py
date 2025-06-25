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
st.set_page_config(page_title="Anime Character Identifier", page_icon="🎌")

st.markdown("<h1 style='text-align: center;'>🎌 Anime Character Identifier</h1>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📤 Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Layout for image + recognition result
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="📷 Uploaded Image", width=180)

    with col2:
        character_name = recognize_character(image)
        character_name = character_name.split("(")[0].strip()
        st.markdown("### 🔍 Recognized Character:")
        st.success(f"`{character_name}`")

        feedback = st.radio("🤔 Is this correct?", ("Yes", "No"))
        if feedback == "No":
            corrected_name = st.text_input("✏️ Enter the correct name:")
            if st.button("✅ Submit Correction"):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{corrected_name}_{timestamp}.jpg"
                image.save(os.path.join("training_data", filename))
                with open("labels.csv", "a") as f:
                    f.write(f"{corrected_name},{filename}\n")
                st.success("Correction saved for training!")

        character_name = st.text_input("📎 Proceed with character:", value=character_name)

    st.markdown("---")

    if st.button("📄 Get Character Info"):
        with st.spinner("Fetching details... please wait..."):
            result = fetch_character_info(character_name)

            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                # Character Header
                st.image(result["image_url"], width=180)
                st.markdown(f"## 👤 {result['name']}")
                st.markdown("#### 🧾 About:")
                st.markdown(result["about"] or "_No bio available._")

                # Anime Appearances
                st.markdown("#### 🎞️ Anime Appearances:")
                anime_titles = result["anime"] or ["No known anime."]
                st.markdown("• " + "<br>• ".join(anime_titles), unsafe_allow_html=True)

                # Gallery
                gallery = get_character_images(character_name)
                st.markdown("#### 🖼️ Character Gallery")
                if "error" in gallery:
                    st.info("No additional images available.")
                    if "google_search" in gallery:
                        st.markdown(f"🔎 [Search on Google Images]({gallery['google_search']})")
                else:
                    img_cols = st.columns(len(gallery["images"]))
                    for i, img_url in enumerate(gallery["images"]):
                        with img_cols[i]:
                            st.image(img_url, width=100)

                # Streaming Info
                st.markdown("#### 📺 Where to Watch")
                if anime_titles and anime_titles[0] != "No known anime.":
                    anime_title = anime_titles[0]
                else:
                    anime_title = character_name

                streaming = get_streaming_links(anime_title)
                if "error" in streaming:
                    st.info("ℹ️ Streaming info not available.")
                else:
                    for site, url in streaming["links"].items():
                        st.markdown(f"- [{site}]({url})")

else:
    st.warning("⚠️ Please upload a clear anime character image.")