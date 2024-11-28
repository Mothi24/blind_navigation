# detection.py
import config
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO(config.MODEL_PATH)

def detect_objects(frame):
    results = model(frame)
    detected_objects = []

    for box in results[0].boxes:
        # Each box has an xyxy property for bounding box coordinates
        bbox = box.xyxy[0].tolist()  # Convert tensor to list with 4 elements [x1, y1, x2, y2]
        cls = int(box.cls[0].item())  # Convert class to integer
        detected_objects.append((cls, bbox))

    return detected_objects  # returns list of (class, bounding box) tuples