# 🎎 Anime Characterizer

> *"This project identifies anime characters, fetches their bio and behavior using a hybrid DL model approach. It uses DeepDanbooru (ResNet) for tag-based recognition and OpenAI CLIP for fallback similarity matching. The frontend is built with Streamlit for interactive UI."*

**⚠️ Prerequisites:**
- Python 3.11
- Download the pretrained model files (DeepDanbooru, CLIP embeddings) before running

---

## ⚙️ How It Works
1. Upload an anime image
2. Detect one or more characters
3. Recognize each using DeepDanbooru + CLIP hybrid model
4. Fetch character bio from MyAnimeList (via Jikan API)
5. Show anime appearances and streaming links

---

## 📁 Project Structure
```
anime-characterizer/
├── app.py                        # Main Streamlit UI
├── recognizer.py                # Recognition logic (DeepDanbooru + CLIP)
├── fallback_matcher.py          # CLIP-based fallback matcher
├── fetch_bio.py                 # Jikan API integration
├── streaming_info.py            # Anilist API integration
├── character_gallery.py         # Extra image search and gallery
├── requirements.txt             # Project dependencies
├── models/
│   └── deepdanbooru_model/
│       ├── model.h5
│       ├── project.json
│       └── tags.txt
├── character_db/                # Optional: custom face image DB for CLIP
│   ├── rem.jpg
│   ├── goku.jpg
│   └── ...
├── test_images/                 # Sample input images
│   └── rem.jpg
├── labels.csv                   # User corrections for retraining
└── DeepDanbooru/                # Cloned DeepDanbooru repo
```

---

## ▶️ Run the App
```bash
streamlit run app.py
```

---

## 🔧 Phase-wise Breakdown

### 🔧 Phase 1: Project Setup
- Upload image → identify character using DeepDanbooru
- Fetch and display bio with Jikan API

### 🔧 Phase 2: Use TensorFlow DeepDanbooru
1. Clone:  
```bash
git clone https://github.com/KichangKim/DeepDanbooru.git
cd DeepDanbooru
pip install -r requirements.txt
pip install -e .
```
2. Download model:
[DeepDanbooru Pretrained Model v3](https://github.com/KichangKim/DeepDanbooru/releases/)

### 🔧 Phase 3: Jikan API Integration
- Fetch:
  - ✅ Name & Image
  - ✅ About/Bio
  - ✅ Anime Appearances

### 🔧 Phase 4: Hybrid Recognition (DeepDanbooru + CLIP)
**Fallback Flow:**
```
If DeepDanbooru fails (low confidence)
→ Use CLIP to compare uploaded image with a DB of known character images
→ Return most visually similar result
```

Tools:
```bash
pip install open_clip_torch torchvision torch
```

### ✅ Phase 4.2: Build Embeddings DB (Optional but Recommended)
- Create folder: `character_db/`
- Place 100+ known anime character images
- Run embedding script → saves `.pkl` DB
- OR download prebuilt DB: [Drive link](https://drive.google.com/file/d/1YU-fPbqCfDID1uzOmXEAeSuhRkdyKld3/view)

### 🔧 Phase 5: Where to Watch
- Fetch anime title → query AniList GraphQL API
- Display supported platforms:
  - ✅ Crunchyroll
  - ✅ Netflix
  - ✅ Funimation

**Fallback (Planned)**: Use Google Search for obscure anime

## Yolo Model
  pip install ultralytics


### 🔧 Phase 6: FAISS + CLIP Smart Search (Coming Soon)
- Learn from user corrections
- Search via visual similarity
- Fast image-indexed retrieval using FAISS

---

## 🧠 Future Plans
- [ ] Integrate YOLOv8 for multiple face/character detection
- [ ] Expand character DB (1000+ embeddings)
- [ ] Add retraining support for fine-tuning
- [ ] Host on HuggingFace Spaces or Streamlit Cloud

---

## 🤝 Credits
- DeepDanbooru (KichangKim)
- Jikan API (MyAnimeList)
- AniList API
- OpenAI CLIP

---

## 📞 Contact / Contributions
Feel free to contribute or open an issue.
> Built with ❤️ by Team 18
