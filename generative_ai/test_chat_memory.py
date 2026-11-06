from generative_ai.ollama_service import generate_chat_response

messages = [
    {
        "role": "system",
        "content": "You are an AI career mentor."
    },
    {
        "role": "user",
        "content": "I want to become a Machine Learning Engineer."
    },
    {
        "role": "assistant",
        "content": "You should learn Python, mathematics and ML algorithms."
    },
    {
        "role": "user",
        "content": "Which programming language should I focus on?"
    }
]

answer = generate_chat_response(messages)

print("\nAI Response:\n")
print(answer)