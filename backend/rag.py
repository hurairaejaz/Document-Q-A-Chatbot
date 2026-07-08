from pdf_loader import extract_text_from_pdf
from embeddings import split_text
from embeddings import create_embeddings
from database import store_chunks
from database import search
from llm import generate_answer

def process_pdf(file_path, filename):
    """
    Process uploaded PDF and store embeddings in ChromaDB.
    """
    # Extract text page-wise
    pages = extract_text_from_pdf(file_path)
    # Split into chunks
    chunks = split_text(pages)
    # Generate embeddings
    embeddings = create_embeddings(chunks)
    # Store in ChromaDB
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=filename
    )
    return {
        "message": "PDF processed successfully.",
        "chunks_created": len(chunks)
    }

def ask_question(question):
    """
    Answer user question using RAG.
    """
    # Embed user question
    query_embedding = create_embeddings([
        {
            "page": 0,
            "text": question
        }
    ])[0]
    # Search similar chunks
    results = search(
        query_embedding,
        top_k=5
    )
    if results is None:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }
    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    # Generate answer using Groq
    answer = generate_answer(
        question,
        documents
    )
    return {
        "answer": answer,
        "sources": metadata
    }