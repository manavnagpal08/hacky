import streamlit as st
import pandas as pd
import json
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state
from core.export_engine import ExportEngine

st.set_page_config(page_title="Document Viewer | IDP Platform", page_icon="👁️", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("👁️ Document Viewer")

if not st.session_state.get('current_document'):
    st.info("No document currently selected. Please go to Upload or History to select a document.")
    st.stop()
    
doc = st.session_state['current_document']
st.subheader(f"Viewing: {doc.get('filename')} ({doc.get('classification', 'Unknown')})")

# Export Engine
exporter = ExportEngine()

col1, col2, col3 = st.columns([1, 1, 8])
with col1:
    json_data = exporter.export_to_json(doc)
    st.download_button("📥 Export JSON", data=json_data, file_name=f"{doc.get('filename')}.json", mime="application/json")
    
with col2:
    if doc.get("tables"):
        csv_data = exporter.export_to_csv(doc)
        st.download_button("📥 Export CSV", data=csv_data, file_name=f"{doc.get('filename')}_tables.csv", mime="text/csv")
        
with col3:
    if doc.get("tables"):
        xlsx_data = exporter.export_to_excel(doc)
        st.download_button("📥 Export XLSX", data=xlsx_data, file_name=f"{doc.get('filename')}_tables.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.write("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📄 OCR Text", "📊 Tables", "🧠 Entities", "🖼️ Images (Count)", "💻 JSON Output", "ℹ️ Metadata"])

with tab1:
    st.markdown("### Extracted Text")
    for page in doc.get("pages", []):
        st.markdown(f"**Page {page.get('page')}**")
        st.text_area(f"Text Page {page.get('page')}", value=page.get("ocr", {}).get("full_text", ""), height=300, disabled=True)

with tab2:
    st.markdown("### Extracted Tables")
    if doc.get("tables"):
        for t_idx, table in enumerate(doc.get("tables")):
            st.markdown(f"**Table {t_idx + 1} (Page {table.get('page')})**")
            # We reconstruct DataFrame from raw_data
            raw = table.get("raw_data", [])
            if isinstance(raw, str):
                import json
                try:
                    raw = json.loads(raw)
                except:
                    raw = []
                    
            if raw:
                df = pd.DataFrame(raw[1:], columns=raw[0]) if len(raw) > 1 else pd.DataFrame(raw)
                st.dataframe(df, use_container_width=True)
    else:
        st.info("No tables detected in this document.")

with tab3:
    st.markdown("### Extracted Entities")
    entities = doc.get("entities", {})
    if isinstance(entities, dict) and not entities.get("error"):
        cols = st.columns(2)
        for i, (key, value) in enumerate(entities.items()):
            col = cols[i % 2]
            with col:
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                if isinstance(value, list) and value:
                    for v in value:
                        st.markdown(f"- {v}")
                elif value and not isinstance(value, list):
                    st.markdown(f"- {value}")
                else:
                    st.markdown("- *None found*")
    else:
        st.warning("Entity extraction failed or no entities found.")

with tab4:
    st.markdown("### Extracted Images")
    st.info(f"The system detected {doc.get('images_count', 0)} embedded images during processing.")
    # We didn't save raw images to session state to prevent massive memory usage.
    # In a full implementation, these would be downloaded from Firebase Storage.

with tab5:
    st.markdown("### Structured Output")
    st.json(doc)

with tab6:
    st.markdown("### Document Metadata")
    st.write(f"**Filename:** {doc.get('filename')}")
    st.write(f"**Type:** {doc.get('type')}")
    st.write(f"**Classification:** {doc.get('classification')}")
    if doc.get("storage_url"):
        st.write(f"**Storage Link:** [View Original]({doc.get('storage_url')})")
    
    # Calculate average confidence
    confs = [p.get("ocr", {}).get("average_confidence", 0) for p in doc.get("pages", [])]
    avg_conf = sum(confs) / len(confs) if confs else 0
    st.write(f"**Average OCR Confidence:** {avg_conf:.2f}")
