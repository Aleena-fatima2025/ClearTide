from ultralytics import YOLO

# Load a pre-trained Nano model to act as the base
model = YOLO('yolov8n.pt')

# Train the model on your custom marine dataset
# Adjust epochs based on your dataset size; imgsz 640 is standard
results = model.train(
    data='path/to/your/marine_debris_dataset.yaml',
    epochs=50,
    imgsz=640,
    device=0 # Use '0' for GPU, or 'cpu' if training without a dedicated GPU
)

print("Training complete. Your optimized weights are saved in 'runs/detect/train/weights/best.pt'")
