import os
import requests
from dotenv import load_dotenv

load_dotenv() 
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Use validated model name
API_VERSION = "2023-06-01"

def query_claude(prompt, model=CLAUDE_MODEL, temperature=0.9, max_tokens=1024):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "content-type": "application/json",
        "anthropic-version": API_VERSION
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    if resp.ok:
        return resp.json()["content"][0]["text"]
    else:
        # Return full error for debugging
        return f"[Claude error {resp.status_code}]: {resp.text}"

def summarize_market(user_input, fetchai_out, gemini_out):
    prompt = (
        f"Analyze the market for: {user_input}\n"
        f"FetchAI market insights: {fetchai_out}\n"
        f"Gemini pitch analysis: {gemini_out}\n"
        "Summarize the market gap in 2-3 sentences."
    )
    return query_claude(prompt)

def create_launch_plan(user_input, market_gap_summary):
    prompt = (
        f"Given this idea: {user_input}\n"
        f"And this market gap: {market_gap_summary}\n"
        "Generate a 5-step actionable launch plan, with one risk and one differentiator."
    )
    return query_claude(prompt)

# Test block
if __name__ == "__main__":
    print(summarize_market("Uber for study groups", "Strong competition from X", "Gap in university market"))
    print(create_launch_plan("Uber for study groups", "Gap in university market"))
