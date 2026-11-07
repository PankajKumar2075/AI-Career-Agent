import chromadb
from sentence_transformers import SentenceTransformer

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent ChromaDB client
client = chromadb.PersistentClient(
    path="./generative_ai/rag/chroma_db"
)

# Get existing collection
collection = client.get_or_create_collection(
    name="career_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# Career knowledge documents
documents = [
    "Python is an important programming language for Machine Learning. Learn variables, functions, OOP, NumPy and Pandas.",
    "Machine Learning Engineers should understand supervised learning, unsupervised learning, regression, classification, decision trees and SVM.",
    "Deep Learning includes neural networks, CNN, RNN and frameworks such as PyTorch and TensorFlow.",
    "A Machine Learning portfolio should include projects such as house price prediction, spam detection and customer churn prediction.",
    "Full Stack Developers should learn HTML, CSS, JavaScript, React, Node.js, Express.js and MongoDB.",
    "Data Analysts should learn SQL, Excel, Python, Pandas and data visualization."
]

ids = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5", "doc_6"]

# Generate embeddings
embeddings = model.encode(documents)

print("Embedding shape:", embeddings.shape)

# Store documents and embeddings
# Document metadata
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
    }
]

# Generate embeddings
embeddings = model.encode(documents)

# Store documents, embeddings and metadata
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("Documents and metadata stored successfully!")
print("Total documents:", collection.count())

# Student question
query = "What should I learn to become a Machine Learning Engineer?"

# Generate query embedding
query_embedding = model.encode([query])

# Search ChromaDB
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
        results["distances"][0][i]
    )


# Retrieve stored metadata
results = collection.get(
    ids=["doc_1", "doc_2", "doc_3"],
    include=["documents", "metadatas"]
)

print("\nStored Metadata:")

for i in range(len(results["ids"])):
    print("\nDocument:", results["ids"][i])
    print("Category:", results["metadatas"][i]["category"])
    print("Level:", results["metadatas"][i]["level"])



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