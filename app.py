import streamlit as st
from PIL import Image
from recognizer import recognize_character

st.title("🎌 Anime Character Identifier")

uploaded_file = st.file_uploader("Upload an anime image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    st.info("Processing the image...")
    character_name = recognize_character(image)
    character_name = st.text_input("Detected Character:", value=character_name)


    st.success(f"Identified Character: {character_name}")

    st.subheader("Character Details")
    st.write("Here you can add details about the character, such as their background, abilities, and role in the anime.")
    