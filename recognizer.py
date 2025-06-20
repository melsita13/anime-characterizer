import deepdanbooru as dd
from PIL import Image
import numpy as np
import os

Model_Path = "./models/deepdanbooru_model"

def recognize_character(image: Image.Image) -> str:
    # Convert image to model input format
    image = image.convert("RGB")
    width, height = image.size
    target_size = 512
    ratio = target_size / max(width, height)
    new_size = (int(width * ratio), int(height * ratio))
    image = image.resize(new_size)
    background = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    background.paste(
        image, ((target_size - new_size[0]) // 2, (target_size - new_size[1]) // 2)
    )
    image_array = np.array(background) / 255.0
    image_array = image_array.reshape((1, target_size, target_size, 3))

    # Load model and tags
    try:
        model = dd.project.load_model_from_project(Model_Path, compile_model=False)
        tags = dd.project.load_tags_from_project(Model_Path)
        print(f"[INFO] Loaded {len(tags)} tags")
    except Exception as e:
        print(f"[ERROR] Failed to load model or tags: {e}")
        return "Model Load Error"

    # Predict
    predictions = model.predict(image_array)[0]

    tag_confidence = {tag: predictions[i] for i, tag in enumerate(tags)}
    characters = {
        tag: prob
        for tag, prob in tag_confidence.items()
        if tag.startswith("character:") and prob > 0.3
    }

    if characters:
        top_tag = sorted(characters.items(), key=lambda x: x[1], reverse=True)[0][0]
        name = top_tag.split("character:")[1]
        return name.replace("_", " ").title()
    else:
        return "Unknown Character"