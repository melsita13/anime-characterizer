import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image

# Directory for your training data
TRAIN_DIR = 'scripts/training_data/'
MODEL_SAVE_PATH = 'app/model/trained_model.h5'
LABELS_SAVE_PATH = 'app/model/labels.json'

# Image parameters
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 8
EPOCHS = 10

def train_and_save_model():
    """Trains a simple CNN and saves the model and labels."""
    print("Starting data loading and preprocessing...")
    # Create an image data generator for training
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    # Load images from subdirectories and create batches
    train_generator = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # Get the class indices (mapping from character name to index)
    class_indices = train_generator.class_indices
    # Reverse the map for our labels file
    labels = {str(v): k for k, v in class_indices.items()}

    # Save the labels file for the Flask app
    with open(LABELS_SAVE_PATH, 'w') as f:
        json.dump(labels, f)
    
    num_classes = len(labels)
    print(f"Found {num_classes} classes: {labels}")

    # Build a simple CNN model (we can improve this later)
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print("Starting model training...")
    # Train the model
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE
    )

    # Save the trained model
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")
    print(f"Labels saved to {LABELS_SAVE_PATH}")

if __name__ == '__main__':
    train_and_save_model()