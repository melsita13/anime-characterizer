import streamlit as st
from PIL import Image
import torch
from ultralytics import YOLO
import os
import tempfile
import numpy as np
from utils.character_recognition import recognize_characters
from utils.jikan_api import fetch_character_info
import re

st.set_page_config(page_title="Anime Character Identifier", layout="centered")

# Load YOLOv8 model
yolo_model = YOLO("models/yolov8n.pt")  # Replace with your trained model

# App title
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #6C63FF;'>🎌 Anime Character Identifier</h1>
        <p style='font-size: 17px; color: gray;'>Upload an anime scene → Detect characters → Identify them with AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Upload Anime Image", type=["jpg", "jpeg", "png"])

# Utility: Crop face
def crop_face(image, box):
    x1, y1, x2, y2 = map(int, box)
    return image.crop((x1, y1, x2, y2))

if uploaded_file:
    st.image(uploaded_file, caption="📸 Uploaded Image", use_column_width=True)
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)

    with st.spinner("🔍 Detecting characters..."):
        results = yolo_model.predict(img_np, conf=0.4)
        boxes = results[0].boxes.xyxy.cpu().numpy()

    if len(boxes) == 0:
        st.warning("❌ No characters detected. Try another image.")
    else:
        st.success(f"✅ Detected {len(boxes)} character(s).")

        cropped_faces = [crop_face(img, box) for box in boxes]

        for i, face in enumerate(cropped_faces):
            st.markdown(f"""
                <div style="padding: 20px; margin-top: 30px; margin-bottom: 20px; border-radius: 16px;
                background-color: #f9f9f9; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h4 style='color:#e67300;'>🎭 Character {i+1}</h4>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(face, width=180, caption="🖼️ Cropped Character")

            with col2:
                st.markdown("#### 🔍 AI Predictions")
                character_names = recognize_characters(face, top_k=3)
                character_names = [re.sub(r"\s*\(.*?\)", "", name).strip() for name in character_names]

                if character_names:
                    for name in character_names:
                        st.markdown(f"<span style='color: #28a745;'>✅ <b>{name}</b></span>", unsafe_allow_html=True)

                    # Fetch character info for the best match
                    best_match = character_names[0]
                    with st.spinner("📖 Fetching character bio..."):
                        character_info = fetch_character_info(best_match)

                    if character_info:
                        st.markdown("#### 📘 Character Bio")
                        st.markdown(f"**Name:** {character_info['name']}")
                        st.markdown(f"**Anime:** {character_info['anime']}")
                        st.markdown(f"**About:** {character_info['bio']}")

                        if character_info["image_url"]:
                            st.image(character_info["image_url"], width=150)

                        if character_info.get("streaming") and character_info["streaming"].get("links"):
                            st.markdown("#### 🔗 Streaming Platforms")
                            for site, url in character_info["streaming"]["links"].items():
                                st.markdown(
                                    f"""
                                    <a href="{url}" target="_blank" style="
                                        display: inline-block;
                                        background-color: #007bff;
                                        color: white;
                                        padding: 8px 12px;
                                        margin: 6px 4px;
                                        border-radius: 6px;
                                        text-decoration: none;
                                        font-weight: 500;
                                    ">🌐 Watch on {site}</a>
                                    """,
                                    unsafe_allow_html=True,
                                )
                    else:
                        st.warning("⚠️ Could not fetch bio or streaming info.")
                else:
                    st.warning("🤖 Could not confidently identify character.")

            st.markdown("</div>", unsafe_allow_html=True)
