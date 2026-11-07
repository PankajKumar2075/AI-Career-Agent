
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

from generative_ai.ollama_service import generate_ai_response


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def retrieve_documents(query, top_k=3, category=None):

    query_embedding = model.encode([query])

    search_params = {
        "query_embeddings": query_embedding.tolist(),
        "n_results": min(top_k, collection.count())
    }

    if category:
        search_params["where"] = {
            "category": category
        }

    results = collection.query(**search_params)

    documents = results["documents"][0]

    return documents


def generate_rag_response(query, category=None):

    relevant_documents = retrieve_documents(
        query,
        top_k=3,
        category=category
    )

    if not relevant_documents:
        return "No relevant documents found."

    context = "\n\n".join(relevant_documents)

    prompt = f"""
You are an expert AI Career Mentor.

Answer the student's question using the retrieved knowledge.

RETRIEVED CONTEXT:
{context}

STUDENT QUESTION:
{query}

INSTRUCTIONS:
1. Use retrieved context to answer.
2. Explain concepts in beginner-friendly language.
3. Give practical examples where relevant.
4. Do not invent unsupported facts.
5. If context is insufficient, clearly mention it.
"""

    answer = generate_ai_response(prompt)

    return answer


if __name__ == "__main__":

    question = input("Ask your career question: ")

    category = input(
        "Enter category (Python, Machine Learning, "
        "Deep Learning, Full Stack, Data Analytics) "
        "or press Enter for all: "
    )

    category = category.strip() or None

    answer = generate_rag_response(
        question,
        category=category
    )

    print("\nAI Career Assistant:")
    print(answer)
