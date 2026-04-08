import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

class KnowledgeObject:
    def __init__(self, key: str, value: Any, source: str, confidence: float = 1.0):
        self.key = key
        self.value = value
        self.source = source
        self.confidence = confidence
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "source": self.source,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }

class Memory:
    def __init__(self, storage_path: str = "memory.json"):
        self.storage_path = storage_path
        self.knowledge: Dict[str, KnowledgeObject] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for key, val in data.items():
                        self.knowledge[key] = KnowledgeObject(**val)
            except Exception as e:
                print(f"Error loading memory: {e}")

    def _save(self):
        try:
            data = {key: obj.to_dict() for key, obj in self.knowledge.items()}
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def learn(self, key: str, value: Any, source: str, confidence: float = 1.0):
        obj = KnowledgeObject(key, value, source, confidence)
        self.knowledge[key] = obj
        self._save()

    def recall(self, key: str) -> Optional[KnowledgeObject]:
        return self.knowledge.get(key)

    def search(self, query: str) -> List[KnowledgeObject]:
        # Simple keyword search for now
        results = []
        for key, obj in self.knowledge.items():
            if query.lower() in key.lower() or query.lower() in str(obj.value).lower():
                results.append(obj)
        return results

if __name__ == "__main__":
    mem = Memory()
    mem.learn("Python", "A popular programming language", "Self-knowledge")
    print(f"Recalled: {mem.recall('Python').value}")
