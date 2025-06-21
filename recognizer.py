import deepdanbooru as dd
from PIL import Image
import numpy as np

Model_Path = "./models/deepdanbooru_model"


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
    """Recognizes the character in the given image.

    Args:
        image (Image.Image): The image to recognize the character from.

    Returns:
        str: The name of the recognized character or "Unknown Character".
    """
    image_array = preprocess_image(image)
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
    #  step1: Try to extract character tags
    characters = {
        tag: conf
        for tag, conf in tag_confidence.items()
        if tag.startswith("character:") and conf > 0.3
    }

    if characters:
        best_match = sorted(characters.items(), key=lambda item: item[1], reverse=True)[
            0
        ][0]
        return best_match.split("character:")[1].replace("_", " ").title()

    # step2: If no character tags, try to extract general tags
    probable_names = {
        tag: conf
        for tag, conf in tag_confidence.items()
        if "(" in tag and "_" in tag and conf > 0.5
    }
    if probable_names:
        best_fallback = sorted(
            probable_names.items(), key=lambda item: item[1], reverse=True
        )[0][0]
        return best_fallback.split("(")[0].replace("_", " ").title()

    top_tags = sorted(tag_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
    top_tags_clean = [tag.replace('_',' ').split(":")[-1].title() for tag, _ in top_tags]
    return f"Unknown Character (Top Tags: {', '.join(top_tags_clean)})"
