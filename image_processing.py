import torch
import cv2
import pytesseract
import numpy as np
import re
# Specify the path to the Tesseract executable (adjust this path as necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path for Windows

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'licence_plate_detection.pt')
def remove_non_alphanumeric(input_string):
    # Use regular expression to replace all non-alphanumeric characters with nothing
    result = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return result
def get_licence_number(image_path):
    img = cv2.imread(image_path)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
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
            cv2.imshow('Grayscale Image', cropped_img)
            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()
            height, width = cropped_img.shape[:2]
            new_dimensions = (width // 3, height // 3)
            resized_image = cv2.resize(cropped_img, new_dimensions, interpolation=cv2.INTER_AREA)
            cv2.imshow('Grayscale Image', resized_image)
            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()
            # Preprocess the cropped image (optional, but can improve OCR results)
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Grayscale Image', gray)
            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()
            cv2.adaptiveThreshold(cv2.bilateralFilter(gray, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            # Use Tesseract to extract text from the cropped image
            text = pytesseract.image_to_string(gray,output_type=pytesseract.Output.DICT, config='--psm 7')
            cv2.imshow('Grayscale Image', gray)
            cv2.waitKey(0)  # Wait for a key press to close the window
            cv2.destroyAllWindows()
            # Print the extracted text
            # print(f"Extracted Text from cropped image ({x1}, {y1}, {x2}, {y2}):")
            return text['text']
