# This script will:
# Load each image
# Pass through get_image_embedding()
# Store {character_name: embedding_tensor} into a character_db.pkl file

import os
import torch
import pickle
from PIL import Image
from clip_embedder import get_image_embedding

DB_FOLDER = './character_db'
EMBEDDING_FILE = './character_db/character_embeddings.pkl'

def build_db():
    database = {}

    for filename in os.listdir(DB_FOLDER):
        if filename.lower().endswith(('.jpg','.jpeg','.png')):
            char_name = os.path.splitext(filename)[0].lower()
            image_path = os.path.join(DB_FOLDER, filename)
            print(f"🔄Processing: {char_name}")
            try:
                image = Image.open(image_path).convert("RGB")
                embedding = get_image_embedding(image)
                database[char_name] = embedding
            except Exception as e:
                print(f"❌ Error processing {char_name}: {e}")

    with open(EMBEDDING_FILE, 'wb') as f:
        pickle.dump(database, f)
    
    print(f"✅ Saved {len(database)} character embeddings to {EMBEDDING_FILE}")

if __name__ == "__main__":
    build_db()