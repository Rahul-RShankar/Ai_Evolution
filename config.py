import os
import importlib

# Try to load dotenv, fallback to no-op if not found.
# Using importlib to avoid stubborn linter warnings about missing imports.
try:
    dotenv_module = importlib.import_module("dotenv")
    load_dotenv = getattr(dotenv_module, "load_dotenv")
except (ImportError, AttributeError):
    def load_dotenv(): 
        """Fallback no-op function for when python-dotenv is not installed."""
        pass

load_dotenv()

class Config:
    # LLM Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = "gpt-4-turbo"  # Default model
    
    # Memory & Training
    MEMORY_FILE = "action_memory.json"
    TRAINING_DATA_PATH = "training_data.jsonl"
    ACTIVE_LEARNING_THRESHOLD = 5  # Trigger learning after this many failures
    VECTOR_DB_PATH = "./chroma_db"
    
    # Execution Settings
    SANDBOX_DIR = "./sandbox"
    MAX_TASKS = 10
    AUTO_INSTALL_DEPS = True
    ALLOWED_LIBRARIES = [
        "requests", "pandas", "numpy", "matplotlib", "beautifulsoup4", 
        "tabulate", "flask", "pillow", "yfinance", "axios", "express", "cheerio"
    ]
    FORBIDDEN_LIBRARIES = ["selenium", "pyautogui", "keyboard"]
    
    # Agent Settings
    USER_PROMPT_V1 = "You are the meta-brain... your goal is not just to answer, but to evolve the system."
    BACKGROUND_LEARNING = True
    MAX_FIX_ATTEMPTS = 3
    
    # Resilience & API Settings
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # Seconds
    
    # API Keys & Tokens
    HF_TOKEN = os.getenv("HF_TOKEN", "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")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://127.0.0.1:11434/v1/chat/completions")
    DEFAULT_LOCAL_MODEL = "deepseek-r1:8b"
    
    # Provider Priority: ['huggingface', 'local']
    PROVIDER_PRIORITY = ["huggingface", "local"]
    
    MODEL_FALLBACK_LIST = [
        "meta-llama/Llama-3.2-3B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "microsoft/Phi-3-mini-4k-instruct"
    ]
    
    # LLM Consensus Settings
    USE_CONSENSUS = True
    JUDGE_MODEL = "meta-llama/Llama-3.1-70B-Instruct"
    CONSENSUS_MODELS = [
        "meta-llama/Llama-3.2-1B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "meta-llama/Llama-3.1-8B-Instruct"
    ]


config = Config()

if __name__ == "__main__":
    if not config.OPENAI_API_KEY:
        print("WARNING: OPENAI_API_KEY not found in environment. Please add it to a .env file.")
    else:
        print("Config loaded successfully.")
