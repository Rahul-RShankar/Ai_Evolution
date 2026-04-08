import requests
import json
import os

HF_TOKEN = "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"
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

def test_hf():
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    try:
        print(f"Testing HF API at {HF_API_URL}...")
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=20)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hf()
