# test_learning.py
from infra.self_evolution import evolution_manager
import json
import os

def test_active_learning():
    # 1. Create a dummy failure in action_memory.json if it doesn't have one
    dummy_failure = {
        "task": "Calculate the area of a circle with radius r",
        "code": "area = 3.14 * r",
        "error": "NameError: name 'r' is not defined",
        "success": False,
        "status": "INVALIDATED"
    }
    
    memory_path = "action_memory.json"
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []
    
    data.append(dummy_failure)
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print("Added dummy failure to action_memory.json.")
    
    # 2. Run the learning cycle
    print("Running learning cycle...")
    evolution_manager.run_learning_cycle()
    
    # 3. Check if anything was added to training_data.jsonl
    if os.path.exists("training_data.jsonl"):
        with open("training_data.jsonl", "r") as f:
            lines = f.readlines()
            print(f"Total lines in training_data.jsonl: {len(lines)}")
            # We expect at least the passive log from before + maybe this one if local worked
            # Even if local fails, we verify it tried.
    else:
        print("training_data.jsonl not found.")

if __name__ == "__main__":
    test_active_learning()
