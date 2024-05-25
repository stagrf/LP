import torch
import cv2
import pytesseract

# Specify the path to the Tesseract executable (adjust this path as necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path for Windows

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'licence_plate_detection.pt')

def get_licence_number(image_path):
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

            # Preprocess the cropped image (optional, but can improve OCR results)
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Display the grayscale image
            cv2.imshow('Grayscale Image', gray)
            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()

            # Use Tesseract to extract text from the cropped image
            text = pytesseract.image_to_string(gray)
            # Print the extracted text
            print(f"Extracted Text from cropped image ({x1}, {y1}, {x2}, {y2}):")
            print(text)
            return text

