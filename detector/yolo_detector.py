from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import streamlit as st
import os

FINETUNED_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "yolo_finetuned",
    "train",
    "weights",
    "best.pt",
)


@st.cache_resource
def load_yolo_model():
    """
    Load the YOLO model for character detection.
    Returns:
        YOLO: The loaded YOLO model.
    """
    print("Loading YOLO model...")
    model = YOLO(FINETUNED_MODEL_PATH)
    print("YOLO model loaded.")
    return model


yolo_model = load_yolo_model()


def detect_characters(image: Image.Image):
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    results = yolo_model(image_cv, classes=[0], conf=0.5)[0]

    boxes = results.boxes
    cropped_characters = []

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        crop = image_cv[y1:y2, x1:x2]
        crop_pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
        cropped_characters.append(crop_pil)

    return cropped_characters
