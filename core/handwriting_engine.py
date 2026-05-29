from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image

class HandwritingEngine:
    def __init__(self):
        # We load a small model for hackathon speed, but it uses TrOCR
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")
        
    def extract_handwriting(self, image):
        """
        Extracts handwritten text from a cropped image of text.
        Takes a PIL Image.
        """
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return generated_text
