
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from generative_ai.ollama_service import generate_ai_response


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def retrieve_documents(query, top_k=3, category=None, max_distance=0.65):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        where={"category": category} if category else None
    )

    documents = []

    if not results["documents"] or not results["documents"][0]:
        return documents

    for doc, distance, metadata in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0]
    ):
        if distance <= max_distance:
            documents.append({
                "content": doc,
                "source": metadata.get("source", "Unknown"),
                "category": metadata.get("category", "Unknown"),
                "chunk_number": metadata.get("chunk_number"),
                "distance": round(float(distance), 4)
            })

    return documents


def generate_rag_result(query, category=None):

    documents = retrieve_documents(query, category=category)

    if not documents:
        return {
            "answer": "I could not find sufficiently relevant information in the knowledge base. Try rephrasing your question.",
            "sources": [],
            "total_chunks_used": 0
        }

    context = "\n\n".join([
        f"Source: {doc['source']}\n"
        f"Category: {doc['category']}\n"
        f"Content: {doc['content']}"
        for doc in documents
    ])

    prompt = f"""
You are an AI Career Assistant.

Answer the user's question using the provided knowledge base context.

Rules:
1. Give a clear and beginner-friendly answer.
2. Prefer information from the provided context.
3. Do not invent document names or claim that unsupported details came from the documents.
4. If the context does not contain enough information, say so.
5. Use practical examples when appropriate.

KNOWLEDGE BASE CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    answer = generate_ai_response(prompt)

    # Return answer and source information
    return {
        "answer": answer,
        "sources": [
            {
                "source": doc["source"],
                "category": doc["category"],
                "chunk_number": doc["chunk_number"],
                "distance": doc["distance"]
            }
            for doc in documents
        ],
        "total_chunks_used": len(documents)
    }


# Keep the old function for compatibility with existing backend code
def generate_rag_response(query, category=None):
    result = generate_rag_result(query, category)
    return result["answer"]


def inspect_retrieval(query, category=None):

    documents = retrieve_documents(query, category=category)

    print("\n===== RETRIEVED DOCUMENTS =====")

    for doc in documents:
        print("\nSource:", doc["source"])
        print("Category:", doc["category"])
        print("Distance:", doc["distance"])
        print("Content:", doc["content"])


if __name__ == "__main__":

    print("===== SOURCE-AWARE RAG TEST =====")

    question = input("\nEnter your question: ")
    category = input("Enter category (or press Enter for all): ").strip()

    if not category:
        category = None

    result = generate_rag_result(question, category)

    print("\n===== AI ANSWER =====")
    print(result["answer"])

    print("\n===== SOURCE DOCUMENTS =====")

    for source in result["sources"]:
        print("\nSource:", source["source"])
        print("Category:", source["category"])
        print("Chunk:", source["chunk_number"])
        print("Distance:", source["distance"])

    print("\nTotal chunks used:", result["total_chunks_used"])
