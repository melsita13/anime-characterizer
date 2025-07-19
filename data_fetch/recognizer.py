import deepdanbooru as dd
from PIL import Image
import numpy as np
from data_fetch.fallback_matcher import match_with_clip

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
def recognize_characters(image: Image.Image, top_k=3) -> list:
    image_array = preprocess_image(image)

    predictions = model.predict(image_array)[0]
    tag_confidence = {tag: predictions[i] for i, tag in enumerate(tags)}

    # Step 1: Character tags
    characters = {
        tag.split("character:")[1].replace("_", " ").title(): conf
        for tag, conf in tag_confidence.items()
        if tag.startswith("character:") and conf > 0.3
    }

    if characters:
        sorted_characters = sorted(characters.items(), key=lambda x: x[1], reverse=True)
        return [name for name, _ in sorted_characters[:top_k]]

    # Step 2: Anime-style fallback names
    probable_names = {
        tag.split("(")[0].replace("_", " ").title(): conf
        for tag, conf in tag_confidence.items()
        if "(" in tag and "_" in tag and conf > 0.5
    }

    if probable_names:
        sorted_names = sorted(probable_names.items(), key=lambda x: x[1], reverse=True)
        return [name for name, _ in sorted_names[:top_k]]

    # Step 3: CLIP fallback
    best_clip_match, similarity = match_with_clip(image)
    if similarity > 0.65:
        return [f"{best_clip_match} (via CLIP, {similarity:.2f})"]

    return []