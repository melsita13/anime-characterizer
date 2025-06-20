# anime-characterizer

# File Structure
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
# run streamlit
    streamlit run app.py

# phase 2
    1. clone pretrained model
    git clone https://github.com/KichangKim/DeepDanbooru.git
    cd DeepDanbooru

    # 3. Install the local version
    pip install -r requirements.txt
    pip install -e .

