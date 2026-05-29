# AI Intelligent Document Processing (IDP) Platform

A complete, hackathon-winning Intelligent Document Processing platform built with Streamlit, Firebase, and state-of-the-art AI models.

## Features
- **Document Processing**: PDF and image support.
- **OCR**: PaddleOCR for printed text, TrOCR for handwriting.
- **Table Extraction**: Automated detection and extraction using pdfplumber/transformers.
- **Entity Extraction**: Automated identification of key entities (Dates, Amounts, Organizations, etc.).
- **Classification**: AI-powered document classification.
- **AI Chat (RAG)**: Ask questions directly against your documents using FAISS and OpenAI.
- **Analytics & History**: Complete dashboard with KPI metrics and document history.
- **Enterprise UI**: Custom light-theme SaaS design.

## Setup Instructions

1. **Clone & Install Dependencies**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Firebase Setup**
- Go to the [Firebase Console](https://console.firebase.google.com/).
- Create a new project.
- Enable **Authentication** (Email/Password).
- Enable **Firestore Database**.
- Enable **Storage**.
- Go to Project Settings -> Service Accounts -> Generate new private key.
- Save the JSON file as `firebase_credentials.json` in the root of the project.

3. **Environment Variables (.streamlit/secrets.toml)**
- Create a `.streamlit` folder and a `secrets.toml` file inside it.
- Follow the template in `.streamlit/secrets.toml.example` to add your OpenAI API key and Firebase admin credentials.

4. **Run the Application**
```bash
streamlit run app.py
```
