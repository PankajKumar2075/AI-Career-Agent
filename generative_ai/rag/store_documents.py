
from pathlib import Path

from sentence_transformers import SentenceTransformer

from generative_ai.rag.document_processor import (
    load_all_documents,
    split_into_chunks
)

import chromadb


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to persistent ChromaDB
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)


# Document categories
CATEGORY_MAP = {
    "machine_learning.txt": "Machine Learning",
    "python_guide.txt": "Python",
    "data_science_guide.txt": "Data Analytics",
    "full_stack_guide.txt": "Full Stack",
    "interview_guide.txt": "Interview Preparation"
}


# Load all documents
folder = Path(__file__).resolve().parent / "knowledge_base"

documents = load_all_documents(folder)

ids = []
all_chunks = []
metadatas = []


# Process each document
for document in documents:

    file_name = document["file_name"]
    content = document["content"]

    chunks = split_into_chunks(content)

    category = CATEGORY_MAP.get(file_name, "General")

    for i, chunk in enumerate(chunks, start=1):

        chunk_id = f"{Path(file_name).stem}_chunk_{i}"

        ids.append(chunk_id)
        all_chunks.append(chunk)

        metadatas.append({
            "source": file_name,
            "category": category,
            "chunk_number": i
        })


# Generate embeddings
embeddings = model.encode(all_chunks)


# Remove previous knowledge-base chunks before updating.
# This prevents outdated chunks from remaining after reprocessing.
existing = collection.get(
    where={"source": {"$in": list(CATEGORY_MAP.keys())}},
    include=["metadatas"]
)

if existing["ids"]:
    collection.delete(ids=existing["ids"])


# Store updated chunks
collection.upsert(
    ids=ids,
    documents=all_chunks,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)


print("\n===== DOCUMENT STORAGE COMPLETE =====")

print("Documents loaded:", len(documents))
print("Total chunks stored:", len(all_chunks))
print("ChromaDB collection count:", collection.count())

print("\n===== STORED DOCUMENTS =====")

for document in documents:
    print("-", document["file_name"])

print("\n=====================================")
