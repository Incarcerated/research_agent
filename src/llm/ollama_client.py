import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(prompt: str):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            stream=True,
            timeout=180,
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        return f"Error: {e}"