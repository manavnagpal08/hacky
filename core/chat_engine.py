import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class ChatEngine:
    def __init__(self):
        if "openai" in st.secrets and "api_key" in st.secrets["openai"]:
            self.api_key = st.secrets["openai"]["api_key"]
            self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-3.5-turbo", temperature=0)
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
