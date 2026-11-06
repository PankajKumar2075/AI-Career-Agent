import requests

url = "http://localhost:11434/api/chat"

data = {
    "model": "qwen2.5:3b",
    "messages": [
        {
            "role": "user",
            "content": "Explain what a Machine Learning Engineer does."
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)

result = response.json()

print("\nAI Response:\n")
print(result["message"]["content"])