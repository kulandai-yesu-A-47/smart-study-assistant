
from backend.text_processor import split_text
from backend.vector_store import store_chunks, search_chunks
from backend.ai_service import generate_response


def process_document(text):
    chunks = split_text(text)
    document_id = store_chunks(chunks)
    return document_id


def chat_with_document(question, document_id):

    relevant_chunks = search_chunks(
        question,
        document_id=document_id
    )

    if not relevant_chunks:
        return "No relevant information found in this document."

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
    Answer the question using only the document context below.

    If the answer is not available, say:
    "This information is not available in the document."

    Document Context:
    {context}

    Question:
    {question}
    """

    return generate_response(prompt)
