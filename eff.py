import cv2
import numpy as np
import tensorflow as tf

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path=r"E:\krishtech\projects\ESP32\efficientdet_lite0.tflite")
interpreter.allocate_tensors()

# Load label map
with open("coco_labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Get model input details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# Start camera
cap = cv2.VideoCapture(1)  # 0 = Default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    input_image = cv2.resize(frame, (width, height))
    input_tensor = np.expand_dims(input_image, axis=0).astype(np.uint8)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()

    # Get results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]       # Bounding boxes
    classes = interpreter.get_tensor(output_details[1]['index'])[0]     # Class index
    scores = interpreter.get_tensor(output_details[2]['index'])[0]      # Confidence scores

    # Draw results
    for i in range(len(scores)):
        if scores[i] > 0.4:  # Only show detections with confidence > 40%
            ymin, xmin, ymax, xmax = boxes[i]
            x1, y1 = int(xmin * frame.shape[1]), int(ymin * frame.shape[0])
            x2, y2 = int(xmax * frame.shape[1]), int(ymax * frame.shape[0])
            class_id = int(classes[i])
            label = labels[class_id]

            # Print the predicted label
            print(f"Detected: {label}")

            # Draw box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {scores[i]:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("EfficientDet-Lite0 Real-Time Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
