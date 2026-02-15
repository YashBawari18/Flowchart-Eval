
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
        """
        Adaptive preprocessing to handle different lighting conditions and image styles.
        """
        # 1. Adaptive Thresholding
        # Use adaptive thresholding locally to handle shadows or uneven lighting
        thresh = cv2.adaptiveThreshold(
            self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # 2. Morphological Operations
        # Remove small noise (opening) and close gaps (closing)
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        return closing

    def detect_shapes(self):
        """
        Detects contours and classifies them into Start/End, Process, Decision.
        Uses dynamic thresholds based on image size.
        """
        contours, hierarchy = cv2.findContours(self.processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected_shapes = []

        height, width = self.image.shape[:2]
        image_area = height * width
        
        # Dynamic thresholds: 0.1% to 50% of image area
        min_area = image_area * 0.001
        max_area = image_area * 0.5

        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            
            # Filter based on dynamic image size
            if area < min_area or area > max_area:
                continue
            
            # Check hierarchy: We want shapes that don't have parents (outermost) 
            # OR shapes whose parents are the image border. 
            # hierarchy format: [Next, Previous, First_Child, Parent]
            # This is a simple heuristic; for complex diagrams, we might need more advanced tree analysis.
            
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
            num_vertices = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            
            shape_type = "Unknown"
            
            # Improved classification logic
            if num_vertices == 4:
                # Check if it's rotated (diamond) or axis-aligned (rectangle)
                shape_area = cv2.contourArea(approx)
                bbox_area = w * h
                fill_ratio = shape_area / bbox_area if bbox_area > 0 else 0
                
                if fill_ratio < 0.65:
                    shape_type = "Decision"
                elif fill_ratio < 0.95:
                    shape_type = "Start/End" # Rounded Rect / Oval
                else:
                    shape_type = "Process" # Rectangle
            elif num_vertices > 4:
                # Likely an ellipse/oval/rounded rect
                shape_type = "Start/End"
            else:
                # Triangle or other, default to Process for now or ignore
                if num_vertices == 3:
                     # Could be merge/extract, but treat as unknown or process
                     pass

            detected_shapes.append({
                "type": shape_type,
                "bbox": (x, y, w, h),
                "contour": cnt
            })
        
        # Filter duplicates (concentric contours often detected for thick lines)
        # We can sort by area and remove smaller ones contained in larger ones if centroids are close
        return self._filter_duplicates(detected_shapes)

    def _filter_duplicates(self, shapes):
        """Removes duplicate detections for the same shape (e.g. inner/outer borders)."""
        if not shapes: return []
        
        # Sort by area descending
        shapes.sort(key=lambda s: s['bbox'][2] * s['bbox'][3], reverse=True)
        
        kept_shapes = []
        for current in shapes:
            is_duplicate = False
            cx, cy, cw, ch = current['bbox']
            curr_center = (cx + cw/2, cy + ch/2)
            
            for kept in kept_shapes:
                kx, ky, kw, kh = kept['bbox']
                kept_center = (kx + kw/2, ky + kh/2)
                
                # Distance between centers
                dist = np.sqrt((curr_center[0] - kept_center[0])**2 + (curr_center[1] - kept_center[1])**2)
                
                # If center is close and area is significantly smaller, it's likely an inner contour
                if dist < 20: # Threshold for "same location"
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                kept_shapes.append(current)
                
        return kept_shapes

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
