
import cv2
import numpy as np
from image_processor import ImageProcessor

def debug_detection(image_path):
    proc = ImageProcessor(image_path)
    shapes = proc.detect_shapes()
    
    print(f"Total shapes detected: {len(shapes)}")
    
    # Draw on original image
    debug_img = proc.image.copy()
    
    for i, shape in enumerate(shapes):
        x, y, w, h = shape['bbox']
        cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(debug_img, f"{i}: {shape['type']}", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Shape {i}: {shape['type']} at {shape['bbox']}")
    
    cv2.imwrite("data/samples/debug_output.png", debug_img)
    cv2.imwrite("data/samples/preprocessed.png", proc.processed)
    print("Debug images saved: debug_output.png, preprocessed.png")

if __name__ == "__main__":
    debug_detection("data/samples/sample_flowchart.png")
