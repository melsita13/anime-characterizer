import os
import csv
import json
import faiss
import torch
from PIL import Image
from clip_embedder import get_image_embedding

# paths
DATA_DIR = "./training_data"
LABELS_FILE = "./training_data/labels.csv"
INDEX_FILE = "./character_db/character_index.faiss"
LABEL_MAP_FILE = "./character_db/index_to_label.json"


images = []
labels = []

with open(LABELS_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        label, filename = row
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            images.append(path)
            labels.append(label)

# Embed all images
embeddings = []
for path in images:
    try:
        img = Image.open(path).convert("RGB")
        emb = get_image_embedding(img)
        embeddings.append(emb)
    except Exception as e:
        print(f"Skipping {path} due to error: {e}")

# Stack all embeddings
embeddings = torch.cat(embeddings, dim=0).numpy().astype("float32")

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save index and label mapping
faiss.write_index(index, INDEX_FILE)

index_to_label = {i: labels[i] for i in range(len(labels))}
with open(LABEL_MAP_FILE, "w") as f:
    json.dump(index_to_label, f)

print(f"Saved index with {len(labels)} entries.")