from ultralytics import YOLO

model = YOLO("yolov8n.pt")

source = 0   # webcam

# Webcam case
if source == 0:
    model.track(source=source, tracker="bytetrack.yaml", conf=0.35, show=True, save=True)

# Image case
elif isinstance(source, str) and source.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
    model.predict(source=source, conf=0.35, show=True, save=True)

# Video case
else:
    model.track(source=source, tracker="bytetrack.yaml", conf=0.35, show=True, save=True)

print("Done. Check runs/ folder.")