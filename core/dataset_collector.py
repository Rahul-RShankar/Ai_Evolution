# core/dataset_collector.py

import json
import os

class DatasetCollector:

    def __init__(self, filename="training_data.jsonl"):
        self.filename = filename

    def collect(self, task, prompt, result, success, user_weight=1.0):
        """
        Capture a single interaction record with an importance weight.
        """
        record = {
            "instruction": f"Perform task: {task}",
            "input": str(prompt),
            "response": str(result),
            "meta": {
                "success": success,
                "weight": user_weight, # Human-verified data gets trust weighting
                "domain": self._determine_domain(task)
            }
        }

        with open(self.filename, "a") as f:
            f.write(json.dumps(record) + "\n")

    def _determine_domain(self, task):
        task_lower = task.lower()
        if "coding" in task_lower or "script" in task_lower:
            return "coding"
        if "research" in task_lower or "search" in task_lower:
            return "research"
        if "business" in task_lower or "automation" in task_lower:
            return "automation"
        return "general"
