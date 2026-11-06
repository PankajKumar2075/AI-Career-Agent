from generative_ai.ollama_service import generate_ai_response

prompt = """
You are an AI career mentor.

Explain the five most important skills
required to become a Machine Learning Engineer.
"""

answer = generate_ai_response(prompt)

print("\nAI Career Mentor Response:\n")
print(answer)