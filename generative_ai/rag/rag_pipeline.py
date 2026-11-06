
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from generative_ai.ollama_service import generate_ai_response


# Step 1: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Step 2: Create our career knowledge base
documents = [
    "Python is an important programming language for Machine Learning. Learn variables, functions, OOP, NumPy and Pandas.",

    "Machine Learning Engineers should understand supervised learning, unsupervised learning, regression, classification, decision trees and SVM.",

    "Deep Learning includes neural networks, CNN, RNN and frameworks such as PyTorch and TensorFlow.",

    "A Machine Learning portfolio should include projects such as house price prediction, spam detection and customer churn prediction.",

    "Full Stack Developers should learn HTML, CSS, JavaScript, React, Node.js, Express.js and MongoDB.",

    "Data Analysts should learn SQL, Excel, Python, Pandas and data visualization."
]


# Step 3: Generate document embeddings
document_embeddings = model.encode(documents)


# Step 4: Retrieve relevant documents
def retrieve_documents(query, top_k=3):

    query_embedding = model.encode([query])

    similarity_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    results = sorted(
        zip(documents, similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [document for document, score in results[:top_k]]


# Step 5: Generate an answer using retrieved context
def generate_rag_response(query):

    relevant_documents = retrieve_documents(query)

    context = "\n".join(relevant_documents)

    prompt = f"""
    You are an expert AI Career Mentor.

    Answer the student's question using the
    following retrieved career knowledge.

    RETRIEVED CONTEXT:
    {context}

    STUDENT QUESTION:
    {query}

    INSTRUCTIONS:
    1. Use the retrieved context to answer.
    2. Explain concepts in beginner-friendly language.
    3. Give practical suggestions where relevant.
    4. Do not invent facts that are not supported
       by the retrieved context.
    5. If the context does not contain enough
       information, clearly say so.
    """

    answer = generate_ai_response(prompt)

    return answer


# Step 6: Test our RAG pipeline
if __name__ == "__main__":

    question = input("Ask your career question: ")

    print("\nGenerating RAG response...\n")

    answer = generate_rag_response(question)

    print("AI Career Assistant:")
    print(answer)
