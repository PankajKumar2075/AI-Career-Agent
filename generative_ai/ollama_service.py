import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def generate_ai_response(prompt):

    data = {
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama connection error: {e}")


def generate_interview_response(prompt):

    data = {
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.2,
            "num_predict": 650
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=240
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama connection error: {e}")


def generate_chat_response(messages):

    data = {
        "model": "qwen2.5:3b",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama connection error: {e}")