from ultralytics import YOLO

DATA_YAML_PATH = "../yolo_data.yaml"
MODEL_PATH = "../yolov8n.pt"
OUTPUT_DIR = "yolo_finetuned"

print("Loading pretrained YOLO model...")
model = YOLO(MODEL_PATH)
print("Starting training...")

print(f"Starting training with data from {DATA_YAML_PATH}...")
model.train(data=DATA_YAML_PATH, epochs=50, imgsz=640, batch=16, project=OUTPUT_DIR)
print("Training completed.")

print("Saving the trained model...")
model.export()
print(f"Trained model saved to {OUTPUT_DIR}.")