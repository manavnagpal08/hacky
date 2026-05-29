from paddleocr import PaddleOCR
import numpy as np
import cv2

class OCREngine:
    def __init__(self, lang='en', use_angle_cls=True):
        # Initialize PaddleOCR
        # use_angle_cls=True helps identify text direction
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=False)
        
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
        
        # Convert back to BGR for PaddleOCR
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

        # Run PaddleOCR
        result = self.ocr.ocr(img_to_ocr, cls=True)
        
        extracted_data = []
        full_text = []
        total_confidence = 0.0
        count = 0
        
        if result and result[0]:
            for line in result[0]:
                box = line[0] # Bounding box
                text = line[1][0] # Text
                conf = line[1][1] # Confidence
                
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
