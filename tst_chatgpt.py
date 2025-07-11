from PIL import Image
import cv2
import pytesseract
import numpy as np

# Load the image
image_path = "pgCaptchaImage022.jpeg"
img = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply threshold to remove background noise
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Optional: remove horizontal lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Invert back if needed
inverted = cv2.bitwise_not(cleaned)

# Use pytesseract to extract text
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
text = pytesseract.image_to_string(inverted, config=custom_config)

print("Extracted Text:", text.strip())
