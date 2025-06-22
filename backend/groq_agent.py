# backend/agents/groq_agent.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def query_groq(prompt):
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",  # or another Groq-supported model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.9
    }
    r = requests.post(endpoint, headers=headers, json=payload, timeout=20)
    data = r.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return str(data)

    
if __name__ == "__main__":
    print(query_groq("Give me a creative tagline for a sleep tracking wearable for college students."))

