
import cv2
import numpy as np

def generate_sample_flowchart(output_path):
    """Generates a clean digital-style flowchart image for testing."""
    img = np.ones((800, 400, 3), dtype=np.uint8) * 255
    
    # 1. Start (Oval approximation)
    cv2.ellipse(img, (200, 100), (80, 40), 0, 0, 360, (0, 0, 0), 2)
    cv2.putText(img, "START", (165, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Arrow 1
    cv2.arrowedLine(img, (200, 140), (200, 200), (0, 0, 0), 2)
    
    # 2. Process (Rectangle)
    cv2.rectangle(img, (100, 200), (300, 260), (0,0,0), 2)
    cv2.putText(img, "INPUT X", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Arrow 2
    cv2.arrowedLine(img, (200, 260), (200, 320), (0, 0, 0), 2)
    
    # 3. Decision (Diamond)
    pts = np.array([[200, 320], [300, 380], [200, 440], [100, 380]], np.int32)
    cv2.polylines(img, [pts], True, (0,0,0), 2)
    cv2.putText(img, "X > 10?", (165, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Arrow 3 (Stop)
    cv2.arrowedLine(img, (200, 440), (200, 500), (0, 0, 0), 2)
    
    # 4. Stop (Oval)
    cv2.ellipse(img, (200, 540), (80, 40), 0, 0, 360, (0, 0, 0), 2)
    cv2.putText(img, "STOP", (170, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    cv2.imwrite(output_path, img)
    print(f"Sample flowchart generated at {output_path}")

if __name__ == "__main__":
    generate_sample_flowchart("/Users/yashsunderbawari/Desktop/Flowchart-Eval/data/samples/sample_flowchart.png")
