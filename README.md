# 🎎 anime-characterizer

    This project mainly focus on identifying anime characters, bio and behavior. Currently the model identifying some popular anime characters and for non popular its suggesting some tags that will identifys the character details. We are using pretrained DL model resnet from DeepDanbooru and showing the user interface using streamlit.

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

# 🔧 Phase 3: