import torch
import cv2

# Load YOLOv5 model from the official repo with the correct repository format
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Make sure you have internet access for the first time

# Load an image using OpenCV
img = cv2.imread(r'C:\Users\rezme\OneDrive\Desktop\LP\LP\yolov5\testare\22930642_3153002898_b-800574812.jpg')
if img is None:
    raise FileNotFoundError('Image not found. Please check the path.')

# Run inference
results = model(img)

# Print results
results.print()  # Print results to the console

# Save results
results.save(save_dir='inference_output')  # Save inference results to 'inference_output' folder

# Show results (OpenCV visualization)
results.show()  # Display the results using OpenCV

# Process results programmatically
for pred in results.pred:
    for det in pred:
        # Each 'det' is a tensor with (x1, y1, x2, y2, confidence, class)
        x1, y1, x2, y2, conf, cls = det[:6]
        print(f'Bounding box: ({x1:.2f}, {y1:.2f}), ({x2:.2f}, {y2:.2f})')
        print(f'Confidence: {conf:.2f}')
        print(f'Class: {cls:.0f}')
