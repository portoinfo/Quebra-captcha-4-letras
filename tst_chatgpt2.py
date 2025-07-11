import cv2
import numpy as np
import pytesseract

pasta_temp = 'temp_gray'
# Load image
image = cv2.imread("bdcaptcha/pgCaptchaImage001.jpeg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create a mask for blue color (tune if needed)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 160, 0])
upper_blue = np.array([140, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Inpaint to remove the blue line
image_no_line = cv2.inpaint(image, blue_mask, 3, cv2.INPAINT_TELEA)
nome_arquivo = 'image_no_line.jpeg'
cv2.imwrite(f'{pasta_temp}/{nome_arquivo}', image_no_line)

# Convert to grayscale again after line removal
gray_no_line = cv2.cvtColor(image_no_line, cv2.COLOR_BGR2GRAY)
nome_arquivo = 'gray_no_line.jpeg'
cv2.imwrite(f'{pasta_temp}/{nome_arquivo}', gray_no_line)

# Apply thresholding
_, thresh = cv2.threshold(gray_no_line, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Optional: Invert if needed
# thresh = cv2.bitwise_not(thresh)

# OCR configuration
#custom_config = r'--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Extract text using pytesseract
#text = pytesseract.image_to_string(thresh, config=custom_config)

#print("Extracted Text:", text.strip())
