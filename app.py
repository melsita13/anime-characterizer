import streamlit as st
from PIL import Image
from datetime import datetime
import os
from recognizer import recognize_character
from fetch_bio import fetch_character_info
from streaming_info import get_streaming_links
from character_gallery import get_character_images, get_google_image_search

# Create training_data folder if not exists
os.makedirs("training_data", exist_ok=True)

st.title("🎌 Anime Character Identifier")

uploaded_file = st.file_uploader("Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=150)

    # Step 1: Detect character
    character_name = recognize_character(image)
    character_name = character_name.split("(")[0].strip()
    st.subheader("Recognized Character")
    st.write(f"🔍 Detected: `{character_name}`")

    # Feedback: Is this correct?
    feedback = st.radio("Is the recognized character correct?", ("Yes", "No"))
    
    if feedback == "No":
        corrected_name = st.text_input("Enter the correct character name:")
        if st.button("Submit Correction"):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{corrected_name}_{timestamp}.jpg"
            image.save(os.path.join("training_data", filename))
            with open("labels.csv", "a") as f:
                f.write(f"{corrected_name},{filename}\n")
            st.success("✅ Correction saved for training!")

    # Let user still proceed with the current or corrected name
    character_name = st.text_input("Proceed with character:", value=character_name)

    if st.button("Get character info"):
        with st.spinner("Fetching character details..."):
            # Step 2: Fetch bio
            result = fetch_character_info(character_name)

            if "error" in result:
                st.error(result["error"])
            else:
                st.image(result["image_url"], width=200)

                # Step 2.5: Character Gallery
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

                # Step 4: Streaming Info
                streaming = get_streaming_links(character_name)
                st.markdown("### 📺 Where to Watch")
                if "error" in streaming:
                    st.info("Streaming info not available.")
                else:
                    for site, url in streaming["links"].items():
                        st.markdown(f"- [{site}]({url})")
else:
    st.warning("Please upload a clear anime character image.")