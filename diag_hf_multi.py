import requests
import json
import time

HF_TOKEN = "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"
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

models_to_test = [
    "meta-llama/Llama-3.2-3B-Instruct",
    "meta-llama/Llama-3.1-70B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "meta-llama/Llama-3.2-1B-Instruct"
]

def test_models():
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    
    for model in models_to_test:
        print(f"\n--- Testing Model: {model} ---")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'ready'"}],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")
        time.sleep(1)

if __name__ == "__main__":
    test_models()
