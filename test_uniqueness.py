import cv2
import numpy as np
import requests
import json

# 1. Create a dummy image different from sample
# Draw 2 rectangles (Process) and 1 Circle (Start)
img = np.ones((400, 300, 3), dtype=np.uint8) * 255
cv2.rectangle(img, (50, 50), (250, 100), (0, 0, 0), 2) # Process 1 top
cv2.rectangle(img, (50, 150), (250, 200), (0, 0, 0), 2) # Process 2 middle
cv2.circle(img, (150, 300), 40, (0, 0, 0), 2) # Start/End bottom

img_path = 'data/samples/unique_test.png'
cv2.imwrite(img_path, img)

# 2. Analyze it
print(f"Testing with unique image: {img_path}")
with open(img_path, 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5001/analyze', files=files)

data = response.json()
print(json.dumps(data, indent=2))

# 3. Validation Logic
shapes = data['shapes']
print(f"\nShapes Detected: {len(shapes)}")
texts = [s['text'] for s in shapes]
print(f"Texts: {texts}")

# Check if we got expected unique texts
# We expect "Process Step 1", "Process Step 2", "Start" / "End" etc.
if len(set(texts)) == len(texts) and len(texts) > 0:
    print("✅ SUCCESS: All shapes have unique text/IDs!")
else:
    print("❌ FAILURE: Duplicate or missing text detected.")
