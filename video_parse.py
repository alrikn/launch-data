import cv2
import pytesseract
import pandas as pd
import re
import glob
import os

frames_dir = "frames"
image_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))

rows = []

for image_path in image_files:
    img = cv2.imread(image_path)
    if img is None:
        continue

    # Convert to grayscale and improve contrast
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # OCR
    text = pytesseract.image_to_string(gray)

    # Clean common OCR mistakes
    raw = text.replace("°F", "°E").replace("Allitude", "Altitude")

    patterns = {
        "Time_s": r"(\d+\.\d+)\s*s",
        "Latitude": r"(\d+\.\d+°[NS])",
        "Longitude": r"(\d+\.\d+°[EW])",
        "Altitude_km": r"(\d+\.\d+)\s*km",
        "Velocity_km_s": r"(\d+\.\d+)\s*km/s"
    }

    data = {"frame": os.path.basename(image_path)}

    for key, pattern in patterns.items():
        match = re.search(pattern, raw)
        if match:
            data[key] = match.group(1)
        else:
            data[key] = None  # keep column alignment

    rows.append(data)

    print(f"{image_path} -> {data}")

# Save to CSV
df = pd.DataFrame(rows)
df.to_csv("telemetry.csv", index=False)

print("Saved to telemetry.csv")
