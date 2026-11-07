
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer


# 1. Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 2. Create persistent ChromaDB client
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)


# 3. Get existing collection
collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)


# 4. Career knowledge documents
documents = [
    "Python is an important programming language for Machine Learning. Learn variables, functions, OOP, NumPy and Pandas.",

    "Machine Learning Engineers should understand supervised learning, unsupervised learning, regression, classification, decision trees and SVM.",

    "Deep Learning includes neural networks, CNN, RNN and frameworks such as PyTorch and TensorFlow.",

    "A Machine Learning portfolio should include projects such as house price prediction, spam detection and customer churn prediction.",

    "Full Stack Developers should learn HTML, CSS, JavaScript, React, Node.js, Express.js and MongoDB.",

    "Data Analysts should learn SQL, Excel, Python, Pandas and data visualization.",

    "Python supports object-oriented programming using classes and objects. Important concepts include inheritance, polymorphism, encapsulation and abstraction.",

    "NumPy is a Python library for numerical computing. Pandas provides DataFrames for data manipulation. Matplotlib helps create charts and visualizations.",

    "Python exception handling uses try, except and finally blocks. File handling allows developers to read and write text and CSV files."
]


# 5. Unique document IDs
ids = [
    "doc_1",
    "doc_2",
    "doc_3",
    "doc_4",
    "doc_5",
    "doc_6",
    "python_doc_7",
    "python_doc_8",
    "python_doc_9"
]


# 6. Document metadata
metadatas = [
    {
        "category": "Python",
        "level": "Beginner",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Machine Learning",
        "level": "Intermediate",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Deep Learning",
        "level": "Advanced",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Machine Learning",
        "level": "Intermediate",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Full Stack",
        "level": "Beginner",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Data Analytics",
        "level": "Beginner",
        "source": "Career Knowledge Base"
    },

    {
        "category": "Python",
        "level": "Beginner",
        "source": "Python Guide"
    },

    {
        "category": "Python",
        "level": "Beginner",
        "source": "Python Guide"
    },

    {
        "category": "Python",
        "level": "Beginner",
        "source": "Python Guide"
    }
]


# 7. Generate embeddings
embeddings = model.encode(documents)

print("Embedding shape:", embeddings.shape)


# 8. Store documents, embeddings and metadata
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\nDocuments and metadata stored successfully!")
print("Total documents:", collection.count())


# 9. Test semantic search
query = "What should I learn to become a Machine Learning Engineer?"

query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)

print("\nStudent Question:")
print(query)

print("\nRelevant Documents:")

for i, document in enumerate(results["documents"][0]):

    print(f"\nResult {i + 1}:")
    print(document)

    print(
        "Distance:",
        round(results["distances"][0][i], 4)
    )


# 10. Retrieve stored metadata
results = collection.get(
    ids=[
        "doc_1",
        "doc_2",
        "doc_3",
        "python_doc_7",
        "python_doc_8",
        "python_doc_9"
    ],
    include=["documents", "metadatas"]
)

print("\nStored Metadata:")

for i in range(len(results["ids"])):

    print("\nDocument:", results["ids"][i])

    print(
        "Category:",
        results["metadatas"][i]["category"]
    )

    print(
        "Level:",
        results["metadatas"][i]["level"]
    )


# 11. Retrieve Python documents only
print("\nMachine Learning Documents Only:")

results = collection.query(
    query_embeddings=model.encode([
        "How do I learn Machine Learning?"
    ]).tolist(),
    n_results=3,
    where={"category": "Machine Learning"}
)

for document in results["documents"][0]:
    print("-", document)


# 12. Retrieve Python category documents
print("\nPython Documents Only:")

results = collection.query(
    query_embeddings=model.encode([
        "Which Python libraries should I learn?"
    ]).tolist(),
    n_results=3,
    where={"category": "Python"}
)

for i, document in enumerate(results["documents"][0]):

    print(f"\nResult {i + 1}:")
    print(document)

    print(
        "Distance:",
        round(results["distances"][0][i], 4)
    )
