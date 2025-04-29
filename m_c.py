from ultralytics import YOLO

# Load your YOLOv8 model
model = YOLO('yolov8s.pt')  # Replace with your model file

# Export to ONNX
model.export(format='onnx')
