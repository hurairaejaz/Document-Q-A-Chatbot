import chromadb
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "..", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings, filename):
    """
    Store chunks into ChromaDB.
    """

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"{filename}_{i}")

        documents.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "file": filename,
            "chunk": chunk["text"]
        })

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas
    )



def search(query_embedding, top_k=5):
    """
    Search similar chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    if not results["documents"]:
        return None

    if len(results["documents"][0]) == 0:
        return None

    return results