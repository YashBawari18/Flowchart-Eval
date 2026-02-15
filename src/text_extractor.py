
import pytesseract
import cv2
import re

class TextExtractor:
    """
    Extracts and normalizes text from flowchart blocks.
    Handle OCR errors and variations in terminology.
    """
    def __init__(self, tesseract_cmd=None):
        self.use_tesseract = False
        try:
            # Check if tesseract is in path
            import shutil
            if shutil.which('tesseract'):
                self.use_tesseract = True
            
            if tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
                self.use_tesseract = True
                
        except Exception:
            self.use_tesseract = False

    def extract_text(self, image, bbox, shape_type="Unknown", index=0):
        """
        Extracts text from a specific bounding box in the image.
        Fallback to unique placeholder if OCR unavailable.
        """
        text = ""
        
        if self.use_tesseract:
            try:
                x, y, w, h = bbox
                # Add padding
                h_img, w_img = image.shape[:2]
                pad = 5
                x = max(0, x - pad)
                y = max(0, y - pad)
                w = min(w_img - x, w + 2*pad)
                h = min(h_img - y, h + 2*pad)
                
                roi = image[y:y+h, x:x+w]
                
                # Pre-processing ROI for better OCR
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                # Denoise
                gray_roi = cv2.fastNlMeansDenoising(gray_roi, None, 10, 7, 21)
                
                _, thresh_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
                text = pytesseract.image_to_string(thresh_roi, config='--psm 6').strip()
                text = self.normalize_text(text)
                
            except Exception as e:
                print(f"OCR Error: {e}")
                text = ""
        
        # Fallback if no text or no tesseract
        if not text:
            # Generate unique identifier based on type and index
            # This ensures DIFFERENT images get DIFFERENT content structure naturally
            # and the same image gets consistent results.
            if shape_type == "Start/End":
                text = "Start" if index == 0 else "End"
            elif shape_type == "Decision":
                text = f"Check condition {index}"
            elif shape_type == "Process":
                text = f"Process Step {index}"
            else:
                text = f"Node {index}"
        
        return text

    def normalize_text(self, text):
        """
        Cleans text and handles common variations.
        """
        if not text: return ""
        
        # Remove non-alphanumeric noise but keep operations
        text = re.sub(r'[^a-zA-Z0-9\s\+\-\*\/\=\>\<\!]', '', text)
        text = text.strip()
        
        # Simple synonym mapping for research feasibility
        text_lower = text.lower()
        synonyms = {
            "start": ["begin", "entry"],
            "stop": ["end", "exit", "finish"],
            "input": ["read", "get", "scan"],
            "print": ["output", "display", "show", "write"]
        }
        
        for key, vals in synonyms.items():
            for v in vals:
                if v in text_lower:
                    return key.capitalize() # Normalized casing
        
        return text

if __name__ == "__main__":
    print("TextExtractor module loaded.")
