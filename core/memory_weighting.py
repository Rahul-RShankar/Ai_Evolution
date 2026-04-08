# core/memory_weighting.py

import time

class WeightedMemory:

    def __init__(self):
        self.memory = []

    def add(self, data, success=True):

        entry = {
            "data": data,
            "weight": 2.0 if success else 0.5,
            "timestamp": time.time()
        }

        self.memory.append(entry)

    def retrieve(self, query=None):
        if not self.memory:
            return []

        # sort by weight + recency
        sorted_mem = sorted(
            self.memory,
            key=lambda x: x["weight"] * (1 / (time.time() - x["timestamp"] + 1)),
            reverse=True
        )

        return [m["data"] for m in sorted_mem[:3]]
