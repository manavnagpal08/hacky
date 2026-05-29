import streamlit as st
import os
import uuid

def init_session_state():
    """Initializes common session state variables."""
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'current_document' not in st.session_state:
        st.session_state['current_document'] = None
    if 'processed_data' not in st.session_state:
        st.session_state['processed_data'] = None
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

def create_temp_dir():
    """Creates a temporary directory for file processing."""
    os.makedirs("temp", exist_ok=True)

def get_temp_file_path(filename):
    """Generates a temporary file path."""
    create_temp_dir()
    unique_filename = f"{uuid.uuid4()}_{filename}"
    return os.path.join("temp", unique_filename)

def check_auth():
    """Checks if the user is authenticated, otherwise stops execution."""
    if not st.session_state.get('user'):
        st.warning("Please log in to access this page.")
        st.stop()
