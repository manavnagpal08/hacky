import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class ChatEngine:
    def __init__(self):
        self.embeddings = None
        self.llm = None
        self.api_key = None
        
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            self.api_key = st.secrets["gemini"]["api_key"]
            self.embeddings = GoogleGenerativeAIEmbeddings(google_api_key=self.api_key, model="models/embedding-001")
            self.llm = ChatGoogleGenerativeAI(google_api_key=self.api_key, model="gemini-1.5-flash", temperature=0)
        else:
            self.api_key = None
            self.embeddings = None
            self.llm = None
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def create_vector_store(self, text):
        """Creates a FAISS vector store from text."""
        if not self.embeddings:
            return None
            
        chunks = self.text_splitter.split_text(text)
        if not chunks:
            return None
            
        vectorstore = FAISS.from_texts(texts=chunks, embedding=self.embeddings)
        return vectorstore
        
    def get_conversation_chain(self, vectorstore):
        """Creates a conversational chain using the vector store."""
        if not self.llm or not vectorstore:
            return None
            
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
