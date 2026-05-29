import streamlit as st
from utils.css_utils import load_css
from utils.helpers import check_auth, init_session_state
from core.chat_engine import ChatEngine
from firebase.firestore_service import FirestoreService

st.set_page_config(page_title="AI Chat | IDP Platform", page_icon="💬", layout="wide")
load_css()
init_session_state()
check_auth()

st.title("💬 AI Chat with Document")

if not st.session_state.get('current_document'):
    st.info("No document currently selected. Please go to Upload or History to select a document.")
    st.stop()
    
doc = st.session_state['current_document']
st.write(f"Ask questions about: **{doc.get('filename')}**")

chat_engine = ChatEngine()
if not chat_engine.api_key:
    st.error("OpenAI API Key is missing. Please add it to your settings.")
    st.stop()

# Initialize Chat Chain if not present for this document
if 'vectorstore' not in st.session_state or st.session_state.get('vectorstore_doc_id') != doc.get('id'):
    with st.spinner("Building Knowledge Base for this document..."):
        text = doc.get('full_text', "")
        if not text:
            st.warning("No text found in this document to chat with.")
            st.stop()
            
        vs = chat_engine.create_vector_store(text)
        st.session_state['vectorstore'] = vs
        st.session_state['vectorstore_doc_id'] = doc.get('id')
        st.session_state['chat_chain'] = chat_engine.get_conversation_chain(vs)
        st.session_state['chat_history'] = []
        
# Display Chat History
for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Chat Input
if prompt := st.chat_input("Ask a question about this document..."):
    # Add user message to UI
    st.session_state['chat_history'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state['chat_chain'].invoke({"question": prompt})
                answer = response['answer']
                st.markdown(answer)
                st.session_state['chat_history'].append({"role": "assistant", "content": answer})
                
                # Optionally save to Firestore
                db = FirestoreService()
                db.save_chat_message(st.session_state['user']['uid'], doc.get('id'), {
                    "question": prompt,
                    "answer": answer
                })
            except Exception as e:
                st.error(f"Error generating response: {e}")
