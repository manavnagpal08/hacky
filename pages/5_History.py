import streamlit as st
import pandas as pd
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state
from firebase.firestore_service import FirestoreService

st.set_page_config(page_title="History | IDP Platform", page_icon="🕒", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("🕒 Document History")
st.write("View and search previously processed documents.")

db = FirestoreService()
docs = db.get_user_documents(st.session_state['user']['uid'])

if not docs:
    st.info("No documents found in history.")
    st.stop()

# Filters
col1, col2 = st.columns(2)
with col1:
    search = st.text_input("Search by filename")
with col2:
    classifications = list(set([d.get("classification", "Unknown") for d in docs]))
    selected_class = st.selectbox("Filter by Classification", ["All"] + classifications)

# Apply filters
filtered_docs = docs
if search:
    filtered_docs = [d for d in filtered_docs if search.lower() in d.get("filename", "").lower()]
if selected_class != "All":
    filtered_docs = [d for d in filtered_docs if d.get("classification") == selected_class]

if not filtered_docs:
    st.warning("No documents match your filters.")
else:
    for doc in filtered_docs:
        with st.container():
            st.markdown(f"""
            <div class="metric-card" style="text-align: left; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="color: var(--primary-color); font-size: 18px; margin-bottom: 5px;">{doc.get('filename')}</h3>
                        <span class="status-badge status-success">{doc.get('classification', 'Unknown')}</span>
                        <span style="color: #64748B; font-size: 14px; margin-left: 10px;">{doc.get('created_at', '')[:10]}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Button to open document
            if st.button(f"Open Document", key=f"btn_{doc.get('id')}"):
                st.session_state['current_document'] = doc
                st.success("Document loaded! Go to the Document Viewer or AI Chat.")
