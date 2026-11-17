import io
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.ai_service import (
    generate_response,
    summarize_text,
    generate_quiz,
    explain_topic
)

from backend.pdf_service import extract_text
from backend.rag_service import process_document, chat_with_document
from backend.study_agent import run_study_agent


app = FastAPI(
    title="AI Smart Study Assistant",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "AI Smart Study Assistant is running!"}


@app.post("/ask")
def ask_ai(request: ChatRequest):
    answer = generate_response(request.prompt)
    return {"answer": answer}


UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# NOTE: these are normal "def" (not "async def") because they call
# blocking code (Ollama / ChromaDB). FastAPI runs them in a thread,
# so the server does not freeze for other requests.
@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_path = UPLOAD_DIR / Path(file.filename).name
    content = file.file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")

    pdf_path.write_bytes(content)

    try:
        text = extract_text(str(pdf_path))
    except Exception:
        pdf_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Invalid or unreadable PDF")

    if not text.strip():
        pdf_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="PDF contains no readable text")

    document_id = process_document(text)

    return {"filename": file.filename, "document_id": document_id}


@app.post("/summarize-pdf")
def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    content = file.file.read()

    try:
        text = extract_text(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or unreadable PDF")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in PDF"
        )

    summary = summarize_text(text)

    return {
        "filename": file.filename,
        "summary": summary
    }


class DocumentChatRequest(BaseModel):
    question: str
    document_id: str


@app.post("/chat-with-document")
def document_chat(request: DocumentChatRequest):

    answer = chat_with_document(
        request.question,
        request.document_id
    )

    return {"answer": answer}


class QuizRequest(BaseModel):
    text: str


@app.post("/generate-quiz")
def create_quiz(request: QuizRequest):
    quiz = generate_quiz(request.text)

    return {
        "quiz": quiz
    }


class StudyPlanRequest(BaseModel):
    subject: str
    hours: int
    days: int


@app.post("/generate-study-plan")
def create_study_plan(request: StudyPlanRequest):

    plan = run_study_agent(
        request.subject,
        request.hours,
        request.days
    )

    return {"study_plan": plan}


class ExplainRequest(BaseModel):
    topic: str


@app.post("/explain-topic")
def explain(request: ExplainRequest):
    explanation = explain_topic(request.topic)

    return {
        "explanation": explanation
    }