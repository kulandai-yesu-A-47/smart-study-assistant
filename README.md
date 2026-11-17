# AI-Powered Smart Study Assistant

An AI-powered learning assistant that helps students understand, summarize, and learn from their study materials.

## Features

1. **AI PDF Summarizer** – Summarizes uploaded PDF documents.
2. **AI Document Chatbot** – Allows users to ask questions about uploaded PDFs using Retrieval-Augmented Generation (RAG).
3. **AI Quiz Generator** – Generates multiple-choice questions from study materials.
4. **AI Study Planner** – Creates and validates personalized study plans using a multi-step AI workflow.
5. **AI Learning Assistant** – Explains topics in simple English.

## Technologies Used

- Python
- FastAPI
- Streamlit
- Ollama
- Qwen 2.5 (3B)
- ChromaDB
- Retrieval-Augmented Generation (RAG)
- Git & GitHub

## Project Structure

```text
smart-study-assistant/
│
├── backend/
│   ├── ai_service.py
│   ├── main.py
│   ├── pdf_service.py
│   ├── rag_service.py
│   ├── study_agent.py
│   ├── text_processor.py
│   └── vector_store.py
│
├── frontend/
│   └── app.py
│
├── .gitignore
└── requirements.txt
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kulandai-yesu-A-47/smart-study-assistant.git
cd smart-study-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv env
env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the AI Model

Install Ollama and download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before starting the application.

### 5. Start the Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

### 6. Start the Frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

Frontend URL: http://localhost:8501

## Project Purpose

This project demonstrates practical applications of Large Language Models, document-based question answering, vector databases, and multi-step AI workflows to support student learning.