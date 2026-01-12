import cv2
import pytesseract
import pandas as pd
import re

# If on Windows, set tesseract path like:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image_path = "telemetry.png"  # your image file
img = cv2.imread(image_path)

# Convert to grayscale and improve contrast
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# OCR
text = pytesseract.image_to_string(gray)
print(text)

# Example expected OCR output:
# Time : 312.0 s
# Latitude : 09.217°N
# Longitude : 081.447°E
# Altitude : 262.3 km
# Velocity : 4.2 km/s

# Parse values
data = {}
patterns = {
    "Time_s": r"Time\s*:\s*([\d.]+)",
    "Latitude": r"Latitude\s*:\s*([0-9.°NSEW]+)",
    "Longitude": r"Longitude\s*:\s*([0-9.°NSEW]+)",
    "Altitude_km": r"Altitude\s*:\s*([\d.]+)",
    "Velocity_km_s": r"Velocity\s*:\s*([\d.]+)"
}

for key, pattern in patterns.items():
    match = re.search(pattern, text)
    if match:
        data[key] = match.group(1)

# Save to CSV
df = pd.DataFrame([data])
df.to_csv("telemetry.csv", index=False)

print("Saved to telemetry.csv")
