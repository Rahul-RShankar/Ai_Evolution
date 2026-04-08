# infra/llm_client.py

import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from config import config
from typing import Any, Dict, List, Optional, Union

def generate(prompt: str) -> str:
    """
    Multi-Provider Resilient Client: HuggingFace -> OpenRouter -> Local (Ollama)
    """
    priority = getattr(config, "PROVIDER_PRIORITY", ["huggingface", "openrouter", "local"])
    
    for provider in priority:
        result = "ERROR: PROVIDER_NOT_IMPLEMENTED"
        if provider == "huggingface":
            result = generate_huggingface(prompt)
        elif provider == "openrouter":
            result = generate_openrouter(prompt)
        elif provider == "local":
            result = generate_local(prompt)
        
        if result and not result.startswith("ERROR:"):
            return result
        
        print(f"[LLM Router] Provider '{provider}' failed: {result}")

    return "ERROR: ALL_PROVIDERS_FAILED"

def generate_huggingface(prompt: str, model: Optional[str] = None) -> str:
    token = getattr(config, "HF_TOKEN", "")
    if not token: return "ERROR: NO_HF_TOKEN"
    
    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    models = [model] if model else getattr(config, "MODEL_FALLBACK_LIST", ["meta-llama/Llama-3.2-3B-Instruct"])
    
    for m in models:
        try:
            payload = {"model": m, "messages": [{"role": "user", "content": prompt}], "max_tokens": 1000}
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            if response.status_code == 402:
                print(f"[LLM Router] HF 402: Payment Required for {m}. Moving to next model/provider.")
                continue # Try next model in fallback list
        except Exception as e:
            pass
    return "ERROR: HF_FAILED"

def generate_openrouter(prompt: str, model: Optional[str] = None) -> str:
    key = getattr(config, "OPENROUTER_API_KEY", "")
    if not key: return "ERROR: NO_OPENROUTER_KEY"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    m = model or "google/gemma-2-9b-it:free" # Default to a free model
    try:
        payload = {"model": m, "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        pass
    return "ERROR: OPENROUTER_FAILED"

def generate_local(prompt: str, model: Optional[str] = None) -> str:
    url = getattr(config, "LOCAL_LLM_URL", "http://localhost:11434/v1/chat/completions")
    m = model or getattr(config, "DEFAULT_LOCAL_MODEL", "deepseek-r1:14b")
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            payload = {"model": m, "messages": [{"role": "user", "content": prompt}], "stream": False}
            response = requests.post(url, json=payload, timeout=90) # Increased timeout
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            
            # Handle "loading model" specifically
            if response.status_code == 500 and "loading model" in response.text:
                print(f"[LLM Client] Model {m} is loading... retry {attempt+1}/{max_retries}")
                time.sleep(20 * (attempt + 1))
                continue
            
            return f"ERROR: LOCAL_FAILED_STATUS_{response.status_code}_TEXT_{response.text[:100]}"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return f"ERROR: LOCAL_FETCH_FAILED_{str(e)}"
    
    return "ERROR: LOCAL_MAX_RETRIES_EXCEEDED"

def generate_consensus(prompt: str, system_prompt: Optional[str] = None) -> Union[Dict[str, str], str]:
    """
    Queries multiple models and uses a judge to select the best response.
    """
    consensus_models = getattr(config, "CONSENSUS_MODELS", [])
    judge_model = getattr(config, "JUDGE_MODEL", "meta-llama/Llama-3.1-70B-Instruct")
    
    if not consensus_models:
        return generate(prompt)

    def fetch_model(model_name):
        res = generate_huggingface(prompt, model=model_name)
        return model_name, res if not res.startswith("ERROR:") else None

    print(f"[Consensus] Querying {len(consensus_models)} models in parallel...")
    with ThreadPoolExecutor(max_workers=len(consensus_models)) as executor:
        results = list(executor.map(fetch_model, consensus_models))
    
    valid_responses = {m: r for m, r in results if r}
    
    if not valid_responses:
        print("[Consensus] No valid parallel responses, falling back to sequential router.")
        return generate(prompt) 

    if len(valid_responses) == 1:
        return list(valid_responses.values())[0]

    options_text = ""
    for i, (m, r) in enumerate(valid_responses.items()):
        options_text += f"--- OPTION {i+1} (Model: {m}) ---\n{r}\n\n"

    judge_prompt = f"""
    System: You are a Lead Technical Judge evaluating AI-generated research and code.
    Select the SINGLE BEST response and explain WHY.
    
    CRITICAL CRITERIA:
    1. FACTUAL DENSITY: Prioritize responses with the most facts/valid code.
    2. RESULT-ORIENTED: Penalize excessive meta-reasoning filler.
    3. STRUCTURE: Prioritize responses with clear formatting.
    
    ORIGINAL PROMPT:
    {prompt}
    
    CANDIDATE RESPONSES:
    {options_text}
    
    Format:
    <reasoning>...</reasoning>
    <winner>...</winner>
    """
    
    print(f"[Consensus] Judging with {judge_model}...")
    judge_raw = generate_huggingface(judge_prompt, model=judge_model)
    
    if judge_raw.startswith("ERROR:"):
        print("[Consensus] Judge failed on HF, falling back to main router.")
        judge_raw = generate(judge_prompt)

    reasoning = ""
    winner = ""
    
    try:
        if "<reasoning>" in judge_raw and "</reasoning>" in judge_raw:
            reasoning = judge_raw.split("<reasoning>")[1].split("</reasoning>")[0].strip()
        if "<winner>" in judge_raw and "</winner>" in judge_raw:
            winner = judge_raw.split("<winner>")[1].split("</winner>")[0].strip()
        else:
            winner = judge_raw
    except:
        winner = judge_raw

    return {"winner": winner, "reasoning": reasoning}
