import json
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class EntityExtractor:
    def __init__(self):
        # We need an API key
        if "openai" in st.secrets and "api_key" in st.secrets["openai"]:
            self.llm = ChatOpenAI(
                api_key=st.secrets["openai"]["api_key"],
                model="gpt-3.5-turbo",
                temperature=0
            )
        else:
            self.llm = None
            
    def extract_entities(self, text):
        """
        Uses LLM to extract structured entities from text.
        """
        if not self.llm:
            return {"error": "OpenAI API key missing."}
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert data extraction AI. Extract the following entities from the text: Names, Email Addresses, Phone Numbers, Dates, Addresses, Invoice Numbers, Monetary Amounts, Organizations. Return ONLY a valid JSON object with these keys. If a key is not found, return an empty list for it."),
            ("user", "TEXT TO ANALYZE:\n\n{text}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            # We truncate text if it's too long to save tokens
            result_str = chain.invoke({"text": text[:10000]})
            # Clean markdown if present
            if result_str.startswith("```json"):
                result_str = result_str[7:-3]
            return json.loads(result_str)
        except Exception as e:
            print(f"Extraction error: {e}")
            return {"error": "Failed to parse entities."}
