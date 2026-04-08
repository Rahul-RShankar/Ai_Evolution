# civilization/identity.py

import json
import os

class Identity:

    def __init__(self, name):
        self.name = name
        self.traits = {
            "risk_taking": 0.5,
            "curiosity": 0.7,
            "efficiency": 0.6
        }
        self._load()

    def evolve(self, success):

        if success:
            self.traits["efficiency"] = min(1.0, self.traits.get("efficiency", 0.6) + 0.05)
        else:
            self.traits["curiosity"] = min(1.0, self.traits.get("curiosity", 0.7) + 0.05)
        
        self.save()

    def save(self):
        filepath = f"{self.name}_identity.json"
        with open(filepath, "w") as f:
            json.dump(self.traits, f)

    def _load(self):
        filepath = f"{self.name}_identity.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    self.traits = json.load(f)
            except Exception:
                pass
