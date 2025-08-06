import os
import torch
import open_clip
from PIL import Image
import streamlit as st

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def get_clip_model():
    """
    Load and return the CLIP model and preprocessing function.
    Uses caching to avoid reloading the model multiple times.
    """
    print("Loading CLIP model (ViT-B-32, laion2b_s34b_b79k)...")
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='laion2b_s34b_b79k'
    )
    model.to(device)
    model.eval()
    print("Model loaded.")
    return model, preprocess

model, preprocess = get_clip_model()

def get_image_embedding(image: Image.Image) -> torch.Tensor:
    """
    Extract a normalized CLIP image embedding from a PIL image.
    Returns: Tensor of shape (1, embedding_dim)
    """
    try:
        image_input = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            features = model.encode_image(image_input)
            features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu()
    except Exception as e:
        print(f"Error embedding image: {e}")
        return None

def get_embedding_from_path(image_path: str) -> torch.Tensor:
    """
    Loads image from path and returns its CLIP embedding.
    """
    if not os.path.exists(image_path):
        print(f"Image path does not exist: {image_path}")
        return None
    try:
        image = Image.open(image_path).convert("RGB")
        return get_image_embedding(image)
    except Exception as e:
        print(f"Failed to process image {image_path}: {e}")
        return None
