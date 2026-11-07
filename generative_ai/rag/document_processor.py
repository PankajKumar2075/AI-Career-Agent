
from pathlib import Path


def load_document(file_path):
    """Read a text document."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def split_into_chunks(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent / "knowledge_base"
    file_path = folder / "machine_learning.txt"

    document = load_document(file_path)

    chunks = split_into_chunks(
        document,
        chunk_size=500,
        overlap=100
    )

    print("Document loaded successfully!")
    print("Total characters:", len(document))
    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)
