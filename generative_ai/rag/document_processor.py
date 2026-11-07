
from pathlib import Path
import re


def load_document(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_all_documents(folder_path):
    documents = []

    folder = Path(folder_path)

    for file_path in folder.glob("*.txt"):
        content = load_document(file_path)

        documents.append({
            "file_name": file_path.name,
            "content": content
        })

    return documents


def split_into_chunks(text, chunk_size=500, overlap=100):
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be non-negative and smaller than chunk size."
        )

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_chunk = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        current_text = " ".join(current_chunk)

        if current_chunk and len(current_text) + len(sentence) + 1 > chunk_size:
            chunks.append(current_text)

            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_chunk):
                if overlap_length + len(previous_sentence) > overlap:
                    break

                overlap_sentences.insert(0, previous_sentence)
                overlap_length += len(previous_sentence)

            current_chunk = overlap_sentences

        current_chunk.append(sentence)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


if __name__ == "__main__":

    folder = Path(__file__).resolve().parent / "knowledge_base"

    documents = load_all_documents(folder)

    print("Total documents loaded:", len(documents))

    for document in documents:

        chunks = split_into_chunks(document["content"])

        print("\nDocument:", document["file_name"])
        print("Total characters:", len(document["content"]))
        print("Total chunks:", len(chunks))

        for i, chunk in enumerate(chunks, start=1):
            print(f"\nChunk {i}:")
            print(chunk)
