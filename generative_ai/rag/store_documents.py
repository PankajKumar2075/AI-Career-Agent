
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

from generative_ai.rag.document_processor import (
    load_document,
    split_into_chunks
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to persistent ChromaDB
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# Locate knowledge document
folder = Path(__file__).resolve().parent / "knowledge_base"
file_path = folder / "machine_learning.txt"

# Load and split document
document = load_document(file_path)

chunks = split_into_chunks(
    document,
    chunk_size=500,
    overlap=100
)

print("Total chunks:", len(chunks))

# Generate unique IDs
ids = [
    f"ml_guide_chunk_{i}"
    for i in range(1, len(chunks) + 1)
]

# Generate embeddings
embeddings = model.encode(chunks)

# Create metadata for every chunk
metadatas = [
    {
        "category": "Machine Learning",
        "source": "machine_learning.txt",
        "chunk_number": i
    }
    for i in range(1, len(chunks) + 1)
]

# Store chunks in ChromaDB
collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\nDocuments stored successfully!")

print("Total documents in collection:", collection.count())
