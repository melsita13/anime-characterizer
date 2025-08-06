import faiss
import json
import numpy as np
import streamlit as st
from clip.clip_embedder import get_image_embedding

INDEX_PATH = "./character_db/character_embeddings.pkl"
LABELS_MAP = "./character_db/character_labels.json"

@st.cache_resource
def load_faiss_index():
    """Load the FAISS index and labels map."""
    print("Loading FAISS index and labels map...")
    index = faiss.read_index(INDEX_PATH)
    with open(LABELS_MAP, "r") as f:
        labels_map = json.load(f)
    print("FAISS index and labels map loaded successfully.")
    return index, labels_map

index, labels_map = load_faiss_index()

def recognize_character(image, top_k: int = 3):
    """Recognize the character in the given image."""
    emb = get_image_embedding(image).numpy().astype("float32")
    D, I = index.search(emb, top_k)
    results = [(labels_map[str(i)], float(d)) for d, i in zip(D[0], I[0])]
    return results if results else None