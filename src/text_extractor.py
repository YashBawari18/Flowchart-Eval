
import pytesseract
import cv2
import re

class TextExtractor:
    """
    Extracts and normalizes text from flowchart blocks.
    Handle OCR errors and variations in terminology.
    """
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image, bbox):
        """
        Extracts text from a specific bounding box in the image.
        """
        x, y, w, h = bbox
        roi = image[y:y+h, x:x+w]
        
        # Pre-processing ROI for better OCR
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        try:
            text = pytesseract.image_to_string(thresh_roi, config='--psm 6').strip()
        except Exception as e:
            text = f"[OCR_ERROR: {str(e)}]"
        
        return self.normalize_text(text)

    def normalize_text(self, text):
        """
        Cleans text and handles common variations.
        """
        # Remove non-alphanumeric noise but keep operations
        text = re.sub(r'[^a-zA-Z0-9\s\+\-\*\/\=\>\<\!]', '', text)
        text = text.lower().strip()
        
        # Simple synonym mapping for research feasibility
        synonyms = {
            "start": ["begin", "entry"],
            "stop": ["end", "exit", "finish"],
            "input": ["read", "get", "scan"],
            "print": ["output", "display", "show", "write"]
        }
        
        for key, vals in synonyms.items():
            for v in vals:
                if v in text:
                    return key
        
        return text

if __name__ == "__main__":
    print("TextExtractor module loaded.")
