import deepdanbooru as dd
from PIL import Image
import numpy as np
from fallback_matcher import match_with_clip

Model_Path = "./models/deepdanbooru_model"

# Load once
model = dd.project.load_model_from_project(Model_Path, compile_model=False)
tags = dd.project.load_tags_from_project(Model_Path)

def preprocess_image(image: Image.Image, size: int = 512) -> np.array:
    image = image.convert("RGB")
    width, height = image.size
    ratio = size / max(width, height)
    new_size = (int(width * ratio), int(height * ratio))
    image = image.resize(new_size)
    background = Image.new("RGB", (size, size), (255, 255, 255))
    background.paste(image, ((size - new_size[0]) // 2, (size - new_size[1]) // 2))
    image_array = np.array(background) / 255.0
    return image_array.reshape((1, size, size, 3))

def recognize_character(image: Image.Image) -> str:
    image_array = preprocess_image(image)

    # Predict
    predictions = model.predict(image_array)[0]
    tag_confidence = {tag: predictions[i] for i, tag in enumerate(tags)}

    # Step 1: Exact character tag
    characters = {
        tag: conf for tag, conf in tag_confidence.items()
        if tag.startswith("character:") and conf > 0.3
    }
    if characters:
        best_match = max(characters, key=characters.get)
        return best_match.split("character:")[1].replace("_", " ").title()

    # Step 2: Tags with anime-style naming
    probable_names = {
        tag: conf for tag, conf in tag_confidence.items()
        if "(" in tag and "_" in tag and conf > 0.5
    }
    if probable_names:
        best_fallback = max(probable_names, key=probable_names.get)
        return best_fallback.split("(")[0].replace("_", " ").title()

    # Step 3: Top generic tags
    top_tags = sorted(tag_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
    top_tags_clean = [tag.replace("_", " ").split(":")[-1].title() for tag, _ in top_tags]

    # Step 4: CLIP fallback
    best_clip_match, similarity = match_with_clip(image)
    if similarity > 0.65:
        return f"{best_clip_match} (via CLIP, {similarity:.2f})"

    return f"Best Guess: {top_tags_clean[0]} (by tag analysis)"