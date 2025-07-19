import torch
import pickle
import torch.nn.functional as F
from clip.clip_embedder import get_image_embedding

with open('../character_db/character_embeddings.pkl', 'rb') as f:
    embedding_db = pickle.load(f)

def match_with_clip(image):
    input_embedding = get_image_embedding(image)

    max_similarity = -1
    best_match = "Unknown"
    
    for name, db_embedding in embedding_db.items():
        sim = F.cosine_similarity(input_embedding, db_embedding).item()
        if sim > max_similarity:
            max_similarity = sim
            best_match = name

    return best_match.title(), max_similarity
