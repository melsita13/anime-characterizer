import streamlit as st
from PIL import Image
from recognizer import recognize_character
from fetch_bio import fetch_character_info

st.title("🎌 Anime Character Identifier")

uploaded_file = st.file_uploader("Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=200)

    st.info("Processing the image...")
    st.subheader("Recognized Character")
    character_name = recognize_character(image)
    character_name = st.text_input("Detected Character:", value=character_name)

    if character_name and character_name != "Unknown Character":
        st.button("Get character info")
        with st.spinner("Fetching character details..."):
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
    else:
        st.warning("Please upload a clear anime character image.")
    # st.success(f"Identified Character: {character_name}")