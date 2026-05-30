import pytesseract
from PIL import Image

class OCREngine:
    def __init__(self, lang='eng'):
        self.lang = lang
        
    def extract_text(self, image):
        """
        Extracts text from a PIL Image using PyTesseract.
        Returns full text, confidence, and bounding boxes in a format similar to EasyOCR.
        """
        # Ensure image is in RGB format for pytesseract
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
        
        extracted_data = []
        full_text = []
        total_confidence = 0.0
        count = 0
        
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])
            
            # Tesseract returns conf=-1 for blocks/paragraphs, so we only want words with conf > 0
            if conf > 0 and text:
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                
                # Format box similarly to EasyOCR: [[x,y], [x+w,y], [x+w,y+h], [x,y+h]]
                box = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
                
                extracted_data.append({
                    "box": box,
                    "text": text,
                    "confidence": conf / 100.0  # normalize to 0.0-1.0
                })
                full_text.append(text)
                total_confidence += (conf / 100.0)
                count += 1
                
        avg_confidence = total_confidence / count if count > 0 else 0.0
        
        return {
            "full_text": " ".join(full_text),
            "average_confidence": avg_confidence,
            "raw_data": extracted_data
        }
