import streamlit as st
import pandas as pd
import plotly.express as px
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state
from firebase.firestore_service import FirestoreService

st.set_page_config(page_title="Analytics | IDP Platform", page_icon="📈", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("📈 Advanced Analytics")
st.write("Deep dive into your document processing metrics.")

db = FirestoreService()
docs = db.get_user_documents(st.session_state['user']['uid'])

if not docs:
    st.info("Not enough data to display analytics.")
    st.stop()

df = pd.DataFrame(docs)
df['created_at'] = pd.to_datetime(df['created_at'])

# Calculate Confidences
confidences = []
for doc in docs:
    if 'pages' in doc:
        for page in doc['pages']:
            if 'ocr' in page and 'average_confidence' in page['ocr']:
                confidences.append({
                    "Date": doc['created_at'][:10],
                    "Filename": doc.get('filename', 'Unknown'),
                    "Confidence": page['ocr']['average_confidence']
                })

df_conf = pd.DataFrame(confidences)

col1, col2 = st.columns(2)

with col1:
    st.subheader("OCR Confidence Distribution")
    if not df_conf.empty:
        fig1 = px.histogram(df_conf, x="Confidence", nbins=20, color_discrete_sequence=["#10B981"])
        fig1.update_layout(xaxis_title="Confidence Score", yaxis_title="Number of Pages")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.write("No confidence data available.")

with col2:
    st.subheader("Processing Volume Over Time")
    df_vol = df.groupby(df['created_at'].dt.date).size().reset_index(name='Count')
    fig2 = px.line(df_vol, x="created_at", y="Count", markers=True, color_discrete_sequence=["#8B5CF6"])
    fig2.update_layout(xaxis_title="Date", yaxis_title="Documents Processed")
    st.plotly_chart(fig2, use_container_width=True)

st.write("---")
st.subheader("Confidence by Document Type")
if 'classification' in df.columns and not df_conf.empty:
    # Merge classification into confidences
    doc_class_map = {d.get('filename'): d.get('classification') for d in docs}
    df_conf['Classification'] = df_conf['Filename'].map(doc_class_map)
    
    fig3 = px.box(df_conf, x="Classification", y="Confidence", color="Classification")
    st.plotly_chart(fig3, use_container_width=True)
