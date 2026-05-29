import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import json

def init_firebase():
    """Initializes Firebase Admin SDK."""
    if not firebase_admin._apps:
        try:
            # Check if we have Streamlit secrets available
            if "firebase" in st.secrets:
                cert = dict(st.secrets["firebase"])
                cred = credentials.Certificate(cert)
                
                # We also need the storage bucket from secrets
                bucket_name = cert.get("storage_bucket", "")
                
                firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_name
                })
            else:
                # Fallback to local json file for development outside Streamlit secrets
                # (Not recommended for production, but good for local hackathon)
                cred_path = "firebase_credentials.json"
                if os.path.exists(cred_path):
                    with open(cred_path) as f:
                        cert = json.load(f)
                    cred = credentials.Certificate(cred_path)
                    bucket_name = cert.get("storage_bucket", "")
                    firebase_admin.initialize_app(cred, {
                        'storageBucket': bucket_name
                    })
                else:
                    st.error("Firebase credentials not found. Please set them in .streamlit/secrets.toml")
                    return False
            return True
        except Exception as e:
            st.error(f"Failed to initialize Firebase: {e}")
            return False
    return True

def get_db():
    if init_firebase():
        return firestore.client()
    return None

def get_storage_bucket():
    if init_firebase():
        return storage.bucket()
    return None
