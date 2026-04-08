# test_router.py
from infra.llm_client import generate, generate_local, generate_openrouter, generate_huggingface
from config import config

def test_hf():
    print("--- Testing Hugging Face ---")
    res = generate_huggingface("Hello, say 'HF worked'")
    print(f"Result: {res}")

def test_openrouter():
    print("\n--- Testing OpenRouter (if key exists) ---")
    res = generate_openrouter("Hello, say 'OpenRouter worked'")
    print(f"Result: {res}")

def test_local():
    print("\n--- Testing Local (Ollama) ---")
    res = generate_local("Hello, say 'Local worked'")
    print(f"Result: {res}")

def test_full_router():
    print("\n--- Testing Full Router Logic ---")
    res = generate("Predict the next prime number after 17.")
    print(f"Result: {res}")

if __name__ == "__main__":
    test_hf()
    test_openrouter()
    test_local()
    test_full_router()
