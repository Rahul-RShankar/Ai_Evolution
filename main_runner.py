import time
import json
from typing import Any, Dict, List
from config import config
from agents.coding_agent import CodingAgent
from task_queue import TaskQueue
from perception import PerceptionAgent
from extractor import KnowledgeExtractor
from memory.memory_store import MemoryStore as Memory
from infra import llm_client

class MetaAgent:
    def __init__(self):
        self.task_queue = TaskQueue()
        from core.executor import execute_code
        self.executor = execute_code # Note: MetaAgent expects a class with execute_python, this might need an adapter
        self.memory = Memory()
        self.perception = PerceptionAgent()
        self.is_running = False
        self.extractor = KnowledgeExtractor(None) # Uses llm_client internally now

    def bootstrap(self):
        """Initial tasks to start the learning process."""
        self.task_queue.add_task("Assess current capabilities", priority=1)
        self.task_queue.add_task("Search for latest AI trends in 2026", priority=2)

    def run_loop(self):
        self.is_running = True
        print("Meta-Brain activated. Entering autonomous loop...")
        
        while self.is_running:
            task = self.task_queue.get_next_task()
            
            if not task:
                print("No tasks in queue. Resting for 10 seconds...")
                time.sleep(10)
                continue

            print(f"--- Processing Task: {task.description} ---")
            
            # Logic flow:
            # 1. Perception: Get context if needed
            # 2. Reasoning: LLM decides what to do (placeholder)
            # 3. Action: Execute code or search
            # 4. Learning: Store results in memory
            
            # Placeholder for LLM reasoning
            result = self.perform_task(task)
            
            if result.get("success"):
                self.task_queue.complete_task(task, result)
                print(f"Task Completed: {task.description}")
            else:
                self.task_queue.fail_task(task, result.get("error", "Unknown error"))
                print(f"Task Failed: {task.description}")

            time.sleep(2)  # Pause between tasks

    def perform_task(self, task) -> Dict[str, Any]:
        """
        Uses the LLM to decide on actions and execute them.
        """
        # We always have a client now via infra.llm_client
        prompt = f"""
        Current Task: {task.description}
        Memory Context: {self.memory.search(task.description)[:2]}
        
        You are an autonomous AI. Decide the next action:
        1. SEARCH: Provide a query.
        2. EXECUTE: Provide Python code to solve or investigate.
        3. LEARN: Extract knowledge from provided text.
        4. REFLECT: Update your goal or add a new task.
        
        Return JSON format: {{"action": "...", "payload": "..."}}
        """

        try:
            response_text = llm_client.generate(prompt)
            # Try to extract JSON from response
            if "{" in response_text and "}" in response_text:
                json_part = response_text[response_text.find("{"):response_text.rfind("}")+1]
                data = json.loads(json_part)
            else:
                data = {"action": "REFLECT", "payload": response_text}
                
            action = data.get("action")
            payload = data.get("payload")

            if action == "SEARCH":
                urls = self.perception.search_web(payload)
                return {"success": True, "data": urls}
            elif action == "EXECUTE":
                result = self.executor.execute_python(payload)
                return result
            elif action == "LEARN":
                extracted_facts = self.extractor.extract(payload, context=task.description)
                for fact in extracted_facts:
                    self.memory.learn(fact.get("key"), fact.get("value"), "LLM Extraction", fact.get("confidence", 1.0))
                return {"success": True, "message": f"Saved {len(extracted_facts)} facts"}
            elif action == "REFLECT":
                self.task_queue.add_task(payload, priority=2)
                return {"success": True, "message": "New goal added"}
            
            return {"success": False, "error": f"Unknown action: {action}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # --- PHASE 2 TESTING ---
    print("=== Phase 2: Memory-Aware Coding Agent Test ===")
    agent = CodingAgent()
    queue = TaskQueue()

    tasks = [
        "calculate factorial of 5",
        "calculate factorial of 6",
        "write fibonacci program",
        "calculate factorial of 5"  # Repeat task to test memory
    ]

    for t_desc in tasks:
        print(f"\nProcessing: {t_desc}")
        result = agent.run(t_desc)
        if result["success"]:
            print(f"Result: {result['output'].strip()}")
        else:
            print(f"Error: {result['error']}")

    print("\n=== Phase 2 Test Complete ===")
