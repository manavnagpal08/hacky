import streamlit as st

def load_css():
    st.markdown("""
        <style>
            /* Base Theme - Light */
            :root {
                --primary-color: #2563EB;
                --background-color: #F8FAFC;
                --text-color: #0F172A;
                --card-bg: #FFFFFF;
                --border-color: #E2E8F0;
                --hover-color: #F1F5F9;
            }
            
            /* General App Styling */
            .stApp {
                background-color: var(--background-color);
                color: var(--text-color);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: var(--card-bg);
                border-right: 1px solid var(--border-color);
            }
            
            /* Cards */
            .metric-card {
                background-color: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                text-align: center;
                transition: transform 0.2s;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .metric-card h3 {
                margin: 0;
                font-size: 14px;
                color: #64748B;
                font-weight: 500;
            }
            .metric-card h2 {
                margin: 10px 0 0 0;
                font-size: 28px;
                color: var(--primary-color);
                font-weight: 600;
            }
            
            /* Status Badge */
            .status-badge {
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
            }
            .status-success { background-color: #DCFCE7; color: #166534; }
            .status-pending { background-color: #FEF9C3; color: #854D0E; }
            
            /* Hide Streamlit Branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Buttons */
            .stButton > button {
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: all 0.2s;
            }
            .stButton > button:hover {
                background-color: #1D4ED8;
                color: white;
            }
            
            /* Upload box */
            [data-testid="stFileUploader"] {
                border: 2px dashed var(--primary-color);
                border-radius: 8px;
                background-color: #EFF6FF;
                padding: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value):
    st.markdown(f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <h2>{value}</h2>
        </div>
    """, unsafe_allow_html=True)
