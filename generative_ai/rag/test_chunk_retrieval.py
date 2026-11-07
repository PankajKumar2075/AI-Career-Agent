
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name="career_knowledge"
)

# Ask a question
question = "Which Python libraries should I learn for Machine Learning?"

# Convert question into embedding
query_embedding = model.encode([question])

# Search relevant chunks
results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3,
    where={
        "source": "machine_learning.txt"
    }
)

# Display retrieved results
print("\nQuestion:", question)

for i, document in enumerate(results["documents"][0], start=1):

    metadata = results["metadatas"][0][i - 1]
    distance = results["distances"][0][i - 1]

    print(f"\n--- Result {i} ---")
    print("Category:", metadata["category"])
    print("Source:", metadata["source"])
    print("Chunk number:", metadata["chunk_number"])
    print("Distance:", round(distance, 4))
    print("Content:", document)
