import fitz  # PyMuPDF
from PIL import Image
import io
import os

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)
        
    def get_num_pages(self):
        return len(self.doc)
        
    def get_metadata(self):
        return self.doc.metadata
        
    def render_page_to_image(self, page_num, dpi=300):
        """Renders a PDF page to a PIL Image."""
        if page_num < 0 or page_num >= len(self.doc):
            return None
            
        page = self.doc[page_num]
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        return Image.open(io.BytesIO(img_data))
        
    def extract_text(self, page_num):
        """Extract native text (if any) from the PDF."""
        page = self.doc[page_num]
        return page.get_text("text")

    def close(self):
        self.doc.close()
