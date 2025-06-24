import os
import torch
import pickle
from PIL import Image
import open_clip

# 🔧 Disable Hugging Face symlink warnings on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# ⚙️ Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ Load CLIP model once
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2b_s34b_b79k'
)
model.to(device)
model.eval()

def get_image_embedding(image: Image.Image) -> torch.Tensor:
    """Extract CLIP embedding from a PIL image."""
    image_input = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu()

# =======================
# 🔄 EMBEDDING DB BUILDER
# =======================

DB_FOLDER = './character_db'
EMBEDDING_FILE = './character_db/character_embeddings.pkl'

def build_db():
    """Embed images and store them as {name: embedding} into a .pkl file"""
    
    # 🧠 Load existing embeddings if any
    if os.path.exists(EMBEDDING_FILE):
        with open(EMBEDDING_FILE, 'rb') as f:
            database = pickle.load(f)
        print(f"🗃️ Loaded existing database with {len(database)} entries.")
    else:
        database = {}
        print("📦 Starting a new character database.")

    # 🔍 Process each image in folder
    for filename in os.listdir(DB_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            char_name = os.path.splitext(filename)[0].lower()

            # Skip already existing entries
            if char_name in database:
                print(f"⏭️ Skipping {char_name} (already exists)")
                continue

            image_path = os.path.join(DB_FOLDER, filename)
            print(f"🔄 Processing: {char_name}")
            try:
                image = Image.open(image_path).convert("RGB")
                embedding = get_image_embedding(image)
                database[char_name] = embedding
            except Exception as e:
                print(f"❌ Error processing {char_name}: {e}")

    # 💾 Save updated database
    with open(EMBEDDING_FILE, 'wb') as f:
        pickle.dump(database, f)

    print(f"✅ Saved {len(database)} character embeddings to {EMBEDDING_FILE}")


if __name__ == "__main__":
    build_db()