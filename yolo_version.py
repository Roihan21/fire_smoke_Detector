from ultralytics import YOLO

# Load model trainingan kamu
model = YOLO("runs/detect/train3/weights/best.pt")

# Print informasi modelnya
print("="*30)
print("INI VERSI MODELNYA:")
model.info()
print("="*30)
