import fitz
import io
from PIL import Image

class ImageEngine:
    def __init__(self):
        pass

    def extract_images_from_pdf(self, pdf_path):
        """
        Extracts embedded images from a PDF.
        Returns a list of dicts: {'page': int, 'image': PIL.Image, 'format': str}
        """
        doc = fitz.open(pdf_path)
        extracted_images = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    extracted_images.append({
                        "page": page_num + 1,
                        "index": img_index,
                        "image": image,
                        "format": image_ext
                    })
                except Exception as e:
                    print(f"Failed to load image xref {xref}: {e}")
                    
        doc.close()
        return extracted_images
