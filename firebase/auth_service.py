import streamlit as st
import requests
from firebase_admin import auth
from firebase.firebase_config import init_firebase

def get_firebase_api_key():
    if "firebase" in st.secrets and "api_key" in st.secrets["firebase"]:
        return st.secrets["firebase"]["api_key"]
    return None

def login_user(email, password):
    """Logs in a user using Firebase REST API."""
    api_key = get_firebase_api_key()
    if not api_key:
        st.error("Firebase API Key is missing. Check secrets.toml")
        return None
        
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return {
            "uid": data["localId"],
            "email": data["email"],
            "token": data["idToken"]
        }
    else:
        st.error(f"Login failed: {response.json().get('error', {}).get('message', 'Unknown error')}")
        return None

def register_user(email, password):
    """Registers a new user using Firebase Admin SDK."""
    init_firebase()
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user.uid
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return None

def logout():
    """Clears the Streamlit session state for the user."""
    if "user" in st.session_state:
        del st.session_state["user"]
