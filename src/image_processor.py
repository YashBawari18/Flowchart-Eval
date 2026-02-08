
import cv2
import numpy as np

class ImageProcessor:
    """
    Handles detection of symbols and arrows in a flowchart image.
    Framed as a feasibility study using heuristic-based CV.
    """
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Could not read image at {image_path}")
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.processed = self.preprocess()

    def preprocess(self):
        """Standard preprocessing: Blur, Threshold, Morphological operations."""
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        # Use simple binary threshold for clean digital images
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
        return thresh

    def detect_shapes(self):
        """
        Detects contours and classifies them into Start/End, Process, Decision.
        Returns a list of dictionaries with shape types and bounding boxes.
        """
        contours, hierarchy = cv2.findContours(self.processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected_shapes = []

        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area < 1000 or area > 40000: # Filter noise and the outer boundary
                continue
            
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            num_vertices = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            
            # Skip very large bounding boxes (likely the entire image)
            if w > self.image.shape[1] * 0.8 or h > self.image.shape[0] * 0.8:
                continue
            
            shape_type = "Unknown"
            aspect_ratio = float(w) / h if h > 0 else 1
            
            # Improved classification logic
            if num_vertices == 4:
                # Check if it's rotated (diamond) or axis-aligned (rectangle)
                # For diamond, the bounding box will be much larger than the actual shape
                shape_area = cv2.contourArea(approx)
                bbox_area = w * h
                fill_ratio = shape_area / bbox_area if bbox_area > 0 else 0
                
                if fill_ratio < 0.7:  # Diamond has lower fill ratio
                    shape_type = "Decision"
                else:
                    shape_type = "Process"
            elif num_vertices > 6:
                # Likely an ellipse/oval
                shape_type = "Start/End"
            
            detected_shapes.append({
                "type": shape_type,
                "bbox": (x, y, w, h),
                "contour": cnt
            })
        
        return detected_shapes

    def detect_arrows(self):
        """
        Detects lines that could be arrows.
        In a research prototype, this uses HoughLinesP and checks for arrowhead nearby.
        """
        lines = cv2.HoughLinesP(self.processed, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=20)
        # For simplicity in this prototype, we return the lines directly
        return lines if lines is not None else []

if __name__ == "__main__":
    # Test stub
    print("ImageProcessor module loaded.")
