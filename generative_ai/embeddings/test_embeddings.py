
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sentences
sentences = [
    "I want to become a Machine Learning Engineer.",
    "I want to work in Artificial Intelligence.",
    "I want to become a Full Stack Developer.",
    "I want to learn frontend and backend development.",
    "I want to learn cooking."
]

# Generate embeddings
embeddings = model.encode(sentences)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(embeddings)

# Display similarity between sentences
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        print("\nSentence 1:", sentences[i])
        print("Sentence 2:", sentences[j])
        print("Similarity:", round(similarity_matrix[i][j], 4))
