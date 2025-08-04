import os
import json
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)

MODEL_PATH = 'app/model/trained_model.h5'
LABELS_PATH = 'app/model/labels.json'
DATABASE_PATH = 'app/database/characters.json'

model = None
labels = None
characters_db = None

def load_resources():
    """Load the model, labels, and database once at the start."""
    global model, labels, characters_db
    try:
        if model is None:
            print("Loading Keras model...")
            model = load_model(MODEL_PATH)

        if labels is None:
            print("Loading labels...")
            with open(LABELS_PATH) as f:
                labels = json.load(f)

        if characters_db is None:
            print("Loading character database...")
            with open(DATABASE_PATH) as f:
                characters_db = json.load(f)

    except Exception as e:
        print(f"Error loading resources: {e}")
        model = None
        labels = None
        characters_db = None

def preprocess_image(image, target_size=(224, 224)):
    """Resize and preprocess the image for the model."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize to [0, 1]
    return image

@app.route("/")
def index():
    """Serve the front-end HTML page."""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """API endpoint to predict the character from an uploaded image."""
    load_resources() # Ensure resources are loaded

    if model is None or labels is None or characters_db is None:
        return jsonify({"error": "Model or data not loaded"}), 500

    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]
        image = Image.open(file.stream)
        
        # Preprocess the image
        processed_image = preprocess_image(image)

        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions)
        
        predicted_character_name = labels.get(str(predicted_class_index))

        # Find character info from the database
        character_info = next((char for char in characters_db if char['name'] == predicted_character_name), None)

        if character_info:
            response = {
                "character": predicted_character_name,
                "confidence": float(confidence),
                "description": character_info.get("description"),
                "anime": character_info.get("anime"),
                "related_images": character_info.get("related_images"),
                "where_to_watch": character_info.get("where_to_watch")
            }
        else:
            response = {
                "character": "Unknown",
                "confidence": float(confidence),
                "message": "Character not found in database."
            }

        return jsonify(response)

if __name__ == "__main__":
    load_resources()
    app.run(debug=True)