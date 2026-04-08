# infra/self_evolution.py

import json
import os
from config import config
from infra import llm_client
from utils.logger import log

class SelfEvolutionManager:
    def __init__(self):
        self.training_path = getattr(config, "TRAINING_DATA_PATH", "training_data.jsonl")
        self.memory_path = getattr(config, "MEMORY_FILE", "action_memory.json")
        self.local_model = getattr(config, "DEFAULT_LOCAL_MODEL", "deepseek-r1:14b")

    def log_success(self, task: str, code: str):
        """Append a successful interaction to the training set."""
        try:
            entry = {
                "instruction": task,
                "input": "",
                "output": f"```python\n{code}\n```"
            }
            with open(self.training_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            log(f"[SelfEvolution] Logged success for task: {str(task)[:50]}...")
        except Exception as e:
            log(f"[SelfEvolution] Error logging success: {e}")

    def run_learning_cycle(self):
        """Review past failures and use DeepSeek-R1 to generate expert solutions."""
        if not os.path.exists(self.memory_path):
            log("[SelfEvolution] No memory file found. Skipping cycle.")
            return

        log("[SelfEvolution] Starting Active Learning Cycle...")
        
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                memory_data = json.load(f)
        except Exception as e:
            log(f"[SelfEvolution] Error reading memory: {e}")
            return

        # Filter for failures or invalidated tasks
        failures = [item for item in memory_data if not item.get("success", True) or item.get("status") == "INVALIDATED"]
        
        if not failures:
            log("[SelfEvolution] No failures found to learn from.")
            return

        log(f"[SelfEvolution] Found {len(failures)} failures. Processing with {self.local_model}...")

        processed_count = 0
        for item in failures:
            task = item.get("task", "")
            error = item.get("error", "Unknown error")
            attempted_code = item.get("code", "")

            if not task: continue

            # Construct the Expert Reflection Prompt
            if attempted_code:
                reflection_prompt = f"""
                System: You are a Senior AI Architect & Expert Programmer.
                The FOLLOWING TASK FAILED in a previous attempt.
                
                TASK: {task}
                PREVIOUS FAILED CODE:
                {attempted_code}
                
                ERROR MESSAGE:
                {error}
                
                YOUR GOAL:
                1. Analyze why the previous code failed.
                2. Provide the PERFECT, production-grade, and robust solution in Python.
                3. Ensure the code is self-contained and avoids interactive calls like `input()`.
                
                Format:
                Return ONLY the fixed code block.
                """
            else:
                reflection_prompt = f"""
                System: You are a Senior AI Architect & Expert Programmer.
                This task could NOT be completed by previous agents.
                
                TASK: {task}
                REASON FOR FAILURE: {error}
                
                YOUR GOAL:
                1. Provide a MASTERFUL, production-grade Python solution for this task.
                2. Ensure the code is self-contained and avoids interactive calls like `input()`.
                
                Format:
                Return ONLY the code block.
                """

            log(f"[SelfEvolution] Reflecting on failure: {str(task)[:50]}...")
            
            # Specifically use the LOCAL model (DeepSeek-R1) for the heavy lifting
            expert_code = llm_client.generate_local(reflection_prompt, model=self.local_model)

            if expert_code and not expert_code.startswith("ERROR:"):
                # Clean code block if LLM included markdown
                if "```" in expert_code:
                    expert_code = expert_code.split("```")[1]
                    if expert_code.startswith("python"): expert_code = expert_code[6:]
                
                self.log_success(f"Expert Refinement: {task}", expert_code.strip())
                processed_count += 1
            else:
                log(f"[SelfEvolution] Failed to generate expert fix for: {str(task)[:30]}. Error: {expert_code}")
                processed_count += 0 # Placeholder

        log(f"[SelfEvolution] Learning cycle complete. Generated {processed_count} expert examples.")

evolution_manager = SelfEvolutionManager()
