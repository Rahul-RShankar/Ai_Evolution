# 🚀 AI Evolution: Autonomous AGI Civilization

Welcome to the **AI Evolution** repository—a self-evolving, multi-agent system designed for autonomous code generation, search-grounded research, and continuous expert reflection.

---

## 🧠 Core Features

### 1. **Autonomous Self-Evolution**
The system learns from its own failures. Using **DeepSeek-R1 (Local)**, the agent reflects on past errors and generates "Expert Corrections" to populate a high-fidelity training dataset.
- **Active Learning**: Run `python train_r1.py` to initiate the Deep Reflection cycle.
- **Passive Logging**: Successful task completions are automatically recorded in [training_data.jsonl](file:///d:/AI_Evolution/training_data.jsonl).

### 2. **Resilient LLM Routing**
A multi-provider fallback system ensuring 99.9% uptime for agent reasoning:
1.  **Hugging Face (Router)**: Primary provider for high-speed inference.
2.  **OpenRouter**: Secondary fallback (optional).
3.  **Local Ollama (DeepSeek-R1)**: Final fallback and primary "teacher" for training sessions.

### 3. **Consensus-Based Generation**
The `CodingAgent` can query multiple models in parallel and use a "Lead Judge" to pick the most robust solution, rewarding information density and factual correctness.

---

## 🛠️ Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **Ollama** (Required for the Training Cycle):
  ```bash
  ollama pull deepseek-r1:8b
  ```

### 2. Environment Setup
Create a `.env` file with the following (optional but recommended):
```bash
HF_TOKEN=your_huggingface_token
OPENROUTER_API_KEY=your_key
PYTHONPATH=.
```

### 3. Running the System

#### **Autonomous Brain**
Starts the continuous loop of curiosity, research, and coding.
```powershell
python main.py
```

#### **Expert Training Mode**
Triggers the R1 reflection cycle to process past failures and improve the model's future capabilities.
```powershell
python train_r1.py
```

---

## 📂 Project Architecture

- **`agents/`**: Core intelligence (Coding, Research, Critic).
- **`infra/`**: The backbone. Includes `llm_client.py` (routing) and `self_evolution.py` (learning).
- **`utils/`**: Shared utilities for logging, execution, and health checks.
- **`action_memory.json`**: The agent's permanent history (source for learning).
- **`training_data.jsonl`**: The expert-curated dataset for future fine-tuning.

---

## 🔒 Safety & Resilience
- **Sandbox Execution**: Code is run in an isolated environment.
- **No-Interactive Policy**: The system is hardcoded to avoid `input()` and interactive calls that cause timeouts.
- **Auto-Retry**: The LLM client includes a 10-tier retry loop with exponential backoff for local model loading.

---
*Generated & Evolving by Antigravity.*
