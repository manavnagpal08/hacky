import streamlit as st
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state

st.set_page_config(page_title="Settings | IDP Platform", page_icon="⚙️", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("⚙️ Platform Settings")

st.markdown("""
<style>
.settings-section {
    background-color: var(--card-bg);
    padding: 20px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='settings-section'>", unsafe_allow_html=True)
    st.subheader("OCR Settings")
    primary_engine = st.selectbox("Primary OCR Engine", ["PaddleOCR", "EasyOCR (Fallback)"])
    enable_handwriting = st.checkbox("Enable Handwriting Extraction (TrOCR)", value=True)
    confidence_threshold = st.slider("Confidence Warning Threshold", 0.0, 1.0, 0.8)
    st.markdown("</div>", unsafe_allow_html=True)
    
with st.container():
    st.markdown("<div class='settings-section'>", unsafe_allow_html=True)
    st.subheader("AI Model Settings")
    llm_model = st.selectbox("LLM Model (Classification & Extraction)", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])
    temperature = st.slider("Model Temperature", 0.0, 1.0, 0.0)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='settings-section'>", unsafe_allow_html=True)
    st.subheader("Export Settings")
    include_raw_images = st.checkbox("Include raw images in JSON export", value=False)
    default_export_format = st.selectbox("Default Table Export Format", ["CSV", "XLSX"])
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("Save Settings", type="primary"):
    # In a full app, we would save these to Firestore user preferences
    st.success("Settings saved successfully! (Mocked for hackathon demo)")
