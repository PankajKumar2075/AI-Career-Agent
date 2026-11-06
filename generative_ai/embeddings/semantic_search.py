
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Create our knowledge base
documents = [
    "Learn Python programming and libraries like NumPy and Pandas.",
    "Study machine learning algorithms like Linear Regression, Decision Trees and SVM.",
    "Learn React.js, Node.js and MongoDB for full stack development.",
    "Learn SQL, Excel and data visualization for data analysis.",
    "Study deep learning, neural networks and natural language processing."
]

# Step 3: Convert documents into embeddings
document_embeddings = model.encode(documents)

# Step 4: Take a user query
query = "How can I become a Full Stack Developer?"

# Step 5: Convert query into an embedding
query_embedding = model.encode([query])

# Step 6: Calculate similarity
similarity_scores = cosine_similarity(
    query_embedding,
    document_embeddings
)[0]

# Step 7: Sort documents by similarity
results = sorted(
    zip(documents, similarity_scores),
    key=lambda x: x[1],
    reverse=True
)

# Step 8: Display the top 3 results
print("User Query:", query)
print("\nMost Relevant Documents:\n")

for i, (document, score) in enumerate(results[:3], start=1):
    print(f"Result {i}")
    print("Document:", document)
    print("Similarity Score:", round(float(score), 4))
    print()
