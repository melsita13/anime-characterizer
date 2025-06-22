# 🎎 anime-characterizer

    "This project mainly focus on identifying anime characters, bio and behavior. Currently the model identifying some popular anime characters and for non popular its suggesting some tags that will identifys the character details. We are using pretrained DL model resnet from DeepDanbooru and showing the user interface using streamlit."

**⚠️ Before running the application download required files and use python 3.11**
    
# ⚙️ Working
    1. Run the the app.py
    2. The page will load in browser
    3. Upload anime image
    4. Character identified with bio and behavior

# 📂 File Structure
    anime-characterizer/
    ├── app.py
    ├── recognizer.py
    ├── fetch_bio.py
    ├── requirements.txt
    ├── .gitignore
    ├── test_images/
    │   └── rem.jpg
    ├── models/
    │   └── deepdanbooru_model/
    │       ├── model.h5
    │       ├── project.json
    │       ├── tags.txt
    ├── DeepDanbooru/
    │   ├── deepdanbooru/
    │   ├── requirements.txt
    │   └── ...

# 🔧 Phase 1: Project Setup & Tech Stack
    1.Upload an anime image
    2.Identify the character using a pretrained model
    3.Fetch that character's bio using the Jikan API (MyAnimeList)
<!-- how to run -->
# ▶️ run streamlit
    streamlit run app.py

# 🔧 Phase 2️⃣ Revised: Using DeepDanbooru ONNX Model
    Install the ONNX wrapper for DeepDanbooru:
    ** pip install deepdanbooru-onnx

# 🔧 Phase 2: Upgrade to DeepDanbooru (TensorFlow Version)
    1. clone pretrained model
    git clone https://github.com/KichangKim/DeepDanbooru.git
    cd DeepDanbooru

    2. Download the pretrained model from url and unzip in model folder 
    (https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/deepdanbooru-v3-20211112-sgd-e28.zip)

    # 3. Install the local version
    pip install -r requirements.txt
    pip install -e .

# 🌐 Phase 3 – Jikan API Integration (MyAnimeList)
    Take the recognized character name (e.g., "Rem") → Query the Jikan API → Display:
    ✅ Character Image
    ✅ About/Bio
    ✅ List of Anime appearances

# 🔧 Phase 4: Hybrid Anime Character Identification Model
    Build a two-layer recognition system:
    1.DeepDanbooru: Recognizes known characters (tag-based)
    2.CLIP-based model: Recognizes unknown characters using facial embeddings & similarity matching

   **⛓️‍💥Hybrid Model Workflow**

    1. Upload anime image
    2. Try DeepDanbooru
         └── If confident match → use result
         └── Else → fallback to Vision Model
               └── Match against known character face embeddings
    3. Return final result to UI

   **🔧 Tools We’ll Use in Phase 4**
    
    1. DeepDanbooru (already integrated)
    2. CLIP (Contrastive Language–Image Pretraining)
    OpenAI’s model to match image ↔ text descriptions

    We'll use it to embed the uploaded image and compare with a precomputed list of known characters

    pip install open_clip_torch torchvision torch
    This installs:
        >open_clip_torch – for CLIP model
        >torchvision – for image preprocessing
        >torch – for running the model

# ✅ Phase 4 – Step 2: Build Character Image Database + Embeddings
    Face Image Database (Optional but powerful)
    You’ll prepare a small DB like:
        character_db/
        ├── rem.jpg
        ├── naruto.jpg
        ├── goku.jpg
        ...
    We precompute embeddings for these using CLIP or ViT.
    And then:
    >Generate CLIP embeddings for each image
    >Save them into a .pkl file for fast comparison during inference

# ✅ Phase 4 – Step 3: Similarity Matching Fallback
    If DeepDanbooru returns “Unknown Character”,
    we’ll fallback to comparing the uploaded image with your character_db/ using CLIP embedding similarity.
    