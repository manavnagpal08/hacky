import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.css_utils import load_css, render_metric_card
from utils.helpers import check_auth, init_session_state
from firebase.firestore_service import FirestoreService

st.set_page_config(page_title="Dashboard | IDP Platform", page_icon="📊", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("📊 Dashboard")
st.write("Overview of document processing metrics and system performance.")
st.write("---")

# Mock data since we might not have real data on first run
db_service = FirestoreService()
analytics = db_service.get_analytics(st.session_state['user']['uid'])
docs = db_service.get_user_documents(st.session_state['user']['uid'])

total_docs = len(docs)
total_pages = analytics.get("total_pages", 0) if analytics else 0
total_tables = analytics.get("total_tables", 0) if analytics else 0
total_images = analytics.get("total_images", 0) if analytics else 0

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1: render_metric_card("Total Documents", total_docs)
with col2: render_metric_card("Pages Processed", total_pages)
with col3: render_metric_card("Tables Extracted", total_tables)
with col4: render_metric_card("Images Extracted", total_images)

st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Document Types")
    if docs:
        types = [d.get("classification", "Unknown") for d in docs]
        df_types = pd.Series(types).value_counts().reset_index()
        df_types.columns = ["Type", "Count"]
        fig = px.pie(df_types, values="Count", names="Type", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No documents processed yet. Upload a document to see analytics.")

with col2:
    st.subheader("Processing History")
    if docs:
        dates = [d.get("created_at", "")[:10] for d in docs if d.get("created_at")]
        df_dates = pd.Series(dates).value_counts().reset_index()
        df_dates.columns = ["Date", "Count"]
        df_dates = df_dates.sort_values("Date")
        fig = px.bar(df_dates, x="Date", y="Count", color_discrete_sequence=["#2563EB"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available.")

st.write("---")
st.subheader("Recent Documents")
if docs:
    df_recent = pd.DataFrame(docs[:5])
    if not df_recent.empty:
        df_display = df_recent[['filename', 'classification', 'created_at']]
        df_display['created_at'] = pd.to_datetime(df_display['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.write("No recent documents.")
