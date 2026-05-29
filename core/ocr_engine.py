import easyocr
import numpy as np
import cv2

class OCREngine:
    def __init__(self, lang='en'):
        # Initialize EasyOCR
        self.reader = easyocr.Reader([lang])
        
    def preprocess_image(self, image):
        """
        OpenCV Preprocessing: Denoise, contrast, deskew.
        Takes a PIL Image and returns a preprocessed numpy array.
        """
        # Convert PIL to OpenCV format (BGR)
        open_cv_image = np.array(image) 
        # Convert RGB to BGR 
        if len(open_cv_image.shape) == 3 and open_cv_image.shape[2] == 3:
            open_cv_image = open_cv_image[:, :, ::-1].copy() 

        # Convert to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, h=10, searchWindowSize=21, templateWindowSize=7)
        
        # Contrast Enhancement (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(denoised)
        
        # Convert back to BGR for EasyOCR
        result = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)
        return result

    def extract_text(self, image, preprocess=True):
        """
        Extracts text from a PIL Image.
        Returns full text, confidence, and bounding boxes.
        """
        if preprocess:
            img_to_ocr = self.preprocess_image(image)
        else:
            img_to_ocr = np.array(image)[:, :, ::-1].copy()

        # Run EasyOCR
        result = self.reader.readtext(img_to_ocr)
        
        extracted_data = []
        full_text = []
        total_confidence = 0.0
        count = 0
        
        for line in result:
            box = [[int(pt[0]), int(pt[1])] for pt in line[0]] # Convert numpy types to int for json serialization
            text = line[1]
            conf = float(line[2])
            
            extracted_data.append({
                "box": box,
                "text": text,
                "confidence": conf
            })
            
            full_text.append(text)
            total_confidence += conf
            count += 1
                
        avg_confidence = total_confidence / count if count > 0 else 0.0
        
        return {
            "full_text": "\n".join(full_text),
            "average_confidence": avg_confidence,
            "raw_data": extracted_data
        }
