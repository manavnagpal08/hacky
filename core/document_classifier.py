import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class DocumentClassifier:
    def __init__(self):
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=st.secrets["gemini"]["api_key"],
                model="gemini-1.5-flash",
                temperature=0
            )
        else:
            self.llm = None
            
    def classify(self, text):
        """Classifies a document based on its text content."""
        if not self.llm:
            return "Unknown (Missing API Key)"
            
        categories = [
            "Invoice", "Resume", "Contract", "Bank Statement", 
            "Government Form", "Medical Report", "Business Report", "Other"
        ]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"Classify the following text into exactly one of these categories: {', '.join(categories)}. Respond with ONLY the category name."),
            ("user", "{text}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            result = chain.invoke({"text": text[:3000]})
            return result.strip()
        except Exception as e:
            print(f"Classification error: {e}")
            return "Error during classification"
