from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from generative_ai.ollama_service import generate_ai_response


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create persistent ChromaDB client
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)


# Access existing collection
collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)


# Retrieve relevant documents
def retrieve_documents(query, top_k=3, category=None):

    query_embedding = model.encode([query])

    # Prepare search parameters
    search_params = {
        "query_embeddings": query_embedding.tolist(),
        "n_results": min(top_k, collection.count())
    }

    # Apply category filter if provided
    if category:
        search_params["where"] = {
            "category": category
        }

    results = collection.query(**search_params)

    return results["documents"][0]


# Generate RAG response
def generate_rag_response(query, category=None):

    relevant_documents = retrieve_documents(
        query,
        top_k=3,
        category=category
    )

    if not relevant_documents:
        return "No relevant documents found in this category."

    context = "\n".join(relevant_documents)

    prompt = f"""
You are an expert AI Career Mentor.

Answer the student's question using the retrieved career knowledge.

RETRIEVED CONTEXT:
{context}

STUDENT QUESTION:
{query}

INSTRUCTIONS:
1. Use the retrieved context to answer.
2. Explain concepts in beginner-friendly language.
3. Give practical suggestions where relevant.
4. Do not invent unsupported facts.
5. If context is insufficient, clearly say so.
"""

    return generate_ai_response(prompt)


# Test the RAG pipeline
if __name__ == "__main__":

    question = input("Ask your career question: ")

    print("\nRetrieving relevant documents...\n")

    documents = retrieve_documents(question)

    print("Retrieved Documents:")

    for document in documents:
        print("-", document)

    print("\nGenerating AI response...\n")

    answer = generate_rag_response(question)

    print("AI Career Assistant:")
    print(answer)


if __name__ == "__main__":

    question = input("Ask your career question: ")

    category = input(
        "Enter category (Python, Machine Learning, Deep Learning, Full Stack, Data Analytics): "
    )

    answer = generate_rag_response(
        question,
        category=category
    )

    print("\nAI Career Assistant:")
    print(answer)