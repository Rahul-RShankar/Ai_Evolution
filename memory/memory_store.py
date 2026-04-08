import json
import os
import time

MEMORY_FILE = "action_memory.json"

class MemoryStore:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)

    def load_all(self):
        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save(self, record):
        data = self.load_all()
        
        # Metadata defaults
        record.setdefault("confidence", 0.7)
        record.setdefault("verified", False)
        record.setdefault("timestamp", time.time())
        record.setdefault("status", "ACTIVE")

        # Conflict Resolution: Shadow older, less accurate records for the same task
        if "task" in record:
            task_name = record["task"].lower()
            for item in data:
                if isinstance(item, dict) and "task" in item and item["task"].lower() == task_name:
                    # If the new record is 'better' (e.g. verified or higher confidence), shadow the old one
                    if record.get("verified") or record["confidence"] >= item.get("confidence", 0.5):
                        item["status"] = "SHADOWED"
                        item["confidence"] = min(item["confidence"], 0.2) # Diminish importance

        data.append(record)

        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def invalidate(self, task_description):
        """Flag existing memory records for a task as 'deprecated' or 'incorrect'."""
        data = self.load_all()
        updated = False
        for item in data:
            if isinstance(item, dict) and "task" in item and task_description.lower() in item["task"].lower():
                item["confidence"] = 0.0
                item["verified"] = False
                item["status"] = "INVALIDATED"
                updated = True
        
        if updated:
            with open(MEMORY_FILE, "w") as f:
                json.dump(data, f, indent=2)
        return updated

    def search(self, query):
        data = self.load_all()
        results = []
        for item in data:
            if isinstance(item, dict) and "task" in item and query.lower() in item["task"].lower():
                # Filter: Only ACTIVE, high-confidence data (Ignore SHADOWED or INVALIDATED)
                if item.get("status") == "ACTIVE" and item.get("confidence", 1.0) > 0.1:
                    results.append(item)

        # Fallback: if no ACTIVE data, maybe look at SHADOWED just in case?
        if not results:
            for item in data:
                if isinstance(item, dict) and "task" in item and query.lower() in item["task"].lower():
                    if item.get("confidence", 1.0) > 0.1:
                        results.append(item)

        # Incredibly explicit index access for strict type checkers
        if len(results) > 3:
            return [results[len(results)-3], results[len(results)-2], results[len(results)-1]]
        return results
