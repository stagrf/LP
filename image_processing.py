import torch
import cv2
import pytesseract

# Specify the path to the Tesseract executable (adjust this path as necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path for Windows

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'yolov5\runs\train\exp5\weights\best.pt')

# Load an image using OpenCV
image_path = r'yolov5\testare\mainimg1-777975585.jpg'
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError('Image not found. Please check the path.')

# Run inference
results = model(img)

# Process results and crop the detected regions
for pred in results.pred:
    for det in pred:
        # Each 'det' is a tensor with (x1, y1, x2, y2, confidence, class)
        x1, y1, x2, y2, conf, cls = det[:6]

        # Convert tensor to int for slicing
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Crop the image using the bounding box coordinates
        cropped_img = img[y1:y2, x1:x2]
        model_read_text = torch.hub.load('ultralytics/yolov5', 'custom', path=r'example.pt')
        results_text = model_read_text(cropped_img)
        results_text.show()
        # Preprocess the cropped image (optional, but can improve OCR results)
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Use Tesseract to extract text from the cropped image
        text = pytesseract.image_to_string(gray)
        # Print the extracted text
        print(f"Extracted Text from cropped image ({x1}, {y1}, {x2}, {y2}):")
        # print(results)

        # Optionally, display the cropped and processed images
        # cv2.imshow(f'Cropped Image {x1}_{y1}_{x2}_{y2}', cropped_img)
        # cv2.imshow(f'Processed Image {x1}_{y1}_{x2}_{y2}', gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
