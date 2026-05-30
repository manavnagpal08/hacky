import streamlit as st
import os
import time
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state, get_temp_file_path
from core.pdf_processor import PDFProcessor
from core.ocr_engine import OCREngine
from core.table_engine import TableEngine
from core.image_engine import ImageEngine
from core.entity_extractor import EntityExtractor
from core.document_classifier import DocumentClassifier
from firebase.storage_service import StorageService
from firebase.firestore_service import FirestoreService

st.set_page_config(page_title="Upload | IDP Platform", page_icon="📤", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("📤 Upload Documents")
st.write("Upload PDFs or Images for intelligent processing.")

uploaded_files = st.file_uploader("Drop files here", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Analyze Documents", type="primary"):
        # Initialize Services
        storage = StorageService()
        db = FirestoreService()
        
        # We wrap engines in try-except in case of local missing deps during hackathon
        try:
            ocr = OCREngine()
            table_eng = TableEngine()
            img_eng = ImageEngine()
            entity_ext = EntityExtractor()
            classifier = DocumentClassifier()
        except Exception as e:
            st.error(f"Failed to initialize AI engines: {e}")
            st.stop()
            
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for file_idx, uploaded_file in enumerate(uploaded_files):
            # 1. Save file locally temp
            status_text.text(f"Processing file {file_idx+1}/{len(uploaded_files)}: {uploaded_file.name} - Initializing...")
            temp_path = get_temp_file_path(uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            file_ext = uploaded_file.name.split('.')[-1].lower()
            doc_data = {
                "filename": uploaded_file.name,
                "type": file_ext,
                "pages": [],
                "tables": [],
                "images": [],
                "full_text": ""
            }
            
            try:
                if file_ext == 'pdf':
                    # Process PDF
                    pdf = PDFProcessor(temp_path)
                    num_pages = pdf.get_num_pages()
                    
                    status_text.text(f"Extracting Images and Tables from {uploaded_file.name}...")
                    progress_bar.progress(10)
                    
                    doc_data["images"] = img_eng.extract_images_from_pdf(temp_path)
                    doc_data["tables"] = table_eng.extract_tables_from_pdf(temp_path)
                    
                    progress_bar.progress(30)
                    
                    for page_num in range(num_pages):
                        status_text.text(f"OCR Processing Page {page_num+1}/{num_pages}...")
                        pil_img = pdf.render_page_to_image(page_num)
                        ocr_result = ocr.extract_text(pil_img)
                        doc_data["pages"].append({
                            "page": page_num + 1,
                            "ocr": ocr_result
                        })
                        doc_data["full_text"] += ocr_result["full_text"] + "\n"
                        progress_bar.progress(30 + int(40 * (page_num+1)/num_pages))
                        
                    pdf.close()
                else:
                    # Process Image directly
                    from PIL import Image
                    status_text.text(f"OCR Processing {uploaded_file.name}...")
                    pil_img = Image.open(temp_path)
                    ocr_result = ocr.extract_text(pil_img)
                    doc_data["pages"].append({
                        "page": 1,
                        "ocr": ocr_result
                    })
                    doc_data["full_text"] = ocr_result["full_text"]
                    progress_bar.progress(70)

                # Entity Extraction & Classification
                status_text.text(f"Extracting Entities and Classifying {uploaded_file.name}...")
                doc_data["entities"] = entity_ext.extract_entities(doc_data["full_text"])
                progress_bar.progress(85)
                
                doc_data["classification"] = classifier.classify(doc_data["full_text"])
                progress_bar.progress(90)
                
                # Upload to Firebase Storage
                status_text.text("Saving to cloud...")
                storage_url = storage.upload_local_file(
                    temp_path, 
                    f"users/{st.session_state['user']['uid']}/{int(time.time())}_{uploaded_file.name}"
                )
                doc_data["storage_url"] = storage_url
                
                import json
                clean_data = doc_data.copy()
                clean_data["images_count"] = len(clean_data.get("images", []))
                if "images" in clean_data:
                    del clean_data["images"] # Don't save raw images to DB
                
                # Firestore does not allow nested arrays. 
                # 1. Remove OCR raw bounding boxes (we don't display them anyway)
                for page in clean_data.get("pages", []):
                    if "ocr" in page and "raw_data" in page["ocr"]:
                        del page["ocr"]["raw_data"]

                # 2. Serialize table raw_data (which is a 2D array) to JSON string
                clean_tables = []
                for t in clean_data.get("tables", []):
                    clean_tables.append({
                        "page": t.get("page", 1),
                        "raw_data": json.dumps(t.get("raw_data", []))
                    })
                clean_data["tables"] = clean_tables
                
                # Save to Firestore
                doc_id = str(int(time.time()))
                db.save_document_metadata(st.session_state['user']['uid'], doc_id, clean_data)
                
                # Update Analytics
                db.update_analytics(st.session_state['user']['uid'], {
                    "total_pages": len(clean_data["pages"]),
                    "total_tables": len(clean_tables),
                    "total_images": clean_data["images_count"]
                })
                
                # Cleanup temp file
                if os.path.exists(temp_path): os.remove(temp_path)
                
                progress_bar.progress(100)
                status_text.text("Processing Complete!")
                st.success(f"Successfully processed {uploaded_file.name} as {doc_data['classification']}")
                
                # Store in session for viewer
                st.session_state['current_document'] = clean_data
                st.session_state['current_document']['id'] = doc_id
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
                if os.path.exists(temp_path): os.remove(temp_path)

        st.info("Head over to the Document Viewer to see the results!")
