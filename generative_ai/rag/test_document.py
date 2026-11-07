from pathlib import Path

# Get the knowledge base directory
folder = Path(__file__).resolve().parent / "knowledge_base"

# Read the document
file_path = folder / "machine_learning.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

print("Document loaded successfully!")
print("\nDocument content:\n")
print(content)

print("\nTotal characters:", len(content))