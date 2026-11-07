
from pathlib import Path
import chromadb

DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection("career_knowledge")


# Retrieve all stored document metadata
results = collection.get(
    include=["documents", "metadatas"]
)

print("\n===== CHROMADB DOCUMENT VERIFICATION =====")

print("Total chunks stored:", len(results["ids"]))

# Group chunks by source
document_summary = {}

for metadata in results["metadatas"]:

    source = metadata.get("source", "Unknown")

    if source not in document_summary:
        document_summary[source] = 0

    document_summary[source] += 1


print("\n===== DOCUMENT SUMMARY =====")

for source, count in document_summary.items():
    print(f"{source}: {count} chunks")


print("\n===== SAMPLE STORED CHUNKS =====")

for i in range(min(5, len(results["ids"]))):

    print("\nChunk ID:", results["ids"][i])
    print("Metadata:", results["metadatas"][i])
    print("Content:", results["documents"][i][:200])

print("\n========================================")
