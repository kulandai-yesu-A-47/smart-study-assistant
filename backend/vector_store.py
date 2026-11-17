import chromadb
import uuid

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="study_documents"
)


def store_chunks(chunks):

    document_id = str(uuid.uuid4())

    for index, chunk in enumerate(chunks):

        collection.add(
            ids=[f"{document_id}_{index}"],
            documents=[chunk],
            metadatas=[{"document_id": document_id}]
        )

    return document_id



def search_chunks(query, document_id, limit=3):

    results = collection.query(
        query_texts=[query],
        n_results=limit,
        where={"document_id": document_id}
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    return results["documents"][0]

