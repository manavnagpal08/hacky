import streamlit as st
from utils.css_utils import load_css
from utils.helpers import init_session_state
from firebase.auth_service import login_user, register_user, logout

st.set_page_config(
    page_title="IDP Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State and CSS
init_session_state()
load_css()

def render_auth_page():
    st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>Intelligent Document Processing Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Extract, Analyze, and Understand Documents with AI</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                st.subheader("Login to your account")
                email = st.text_input("Email", placeholder="admin@example.com")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In")
                
                if submit:
                    if email and password:
                        with st.spinner("Authenticating..."):
                            user_data = login_user(email, password)
                            if user_data:
                                st.session_state['user'] = user_data
                                st.success("Login successful!")
                                st.rerun()
                    else:
                        st.warning("Please enter email and password.")
                        
        with tab2:
            with st.form("register_form"):
                st.subheader("Create a new account")
                new_email = st.text_input("Email", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_password")
                reg_submit = st.form_submit_button("Sign Up")
                
                if reg_submit:
                    if new_email and len(new_password) >= 6:
                        with st.spinner("Creating account..."):
                            uid = register_user(new_email, new_password)
                            if uid:
                                st.success("Account created successfully! You can now log in.")
                    else:
                        st.warning("Please provide a valid email and a password of at least 6 characters.")

def render_welcome_page():
    st.markdown(f"<h1>Welcome back, {st.session_state['user']['email']}</h1>", unsafe_allow_html=True)
    st.write("Please select a page from the sidebar to begin processing documents.")
    
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **Dashboard**: View system metrics and analytics.")
    with col2:
        st.success("📤 **Upload**: Process new PDFs and Images.")
    with col3:
        st.warning("💬 **AI Chat**: Chat with your processed documents.")
        
    if st.button("Logout", type="primary"):
        logout()
        st.rerun()

# Routing
if not st.session_state.get('user'):
    render_auth_page()
else:
    render_welcome_page()
