# test_logging.py
from agents.coding_agent import CodingAgent
import os

def test_passive_logging():
    agent = CodingAgent()
    task = "Write a python function to return the square of a number."
    print(f"Running task: {task}")
    result = agent.run(task)
    
    if result["success"]:
        print("Task succeeded!")
        if os.path.exists("training_data.jsonl"):
            with open("training_data.jsonl", "r") as f:
                lines = f.readlines()
                print(f"Total lines in training_data.jsonl: {len(lines)}")
                if len(lines) > 0:
                    print(f"Latest entry: {lines[-1]}")
                else:
                    print("Error: training_data.jsonl is empty!")
        else:
            print("Error: training_data.jsonl does not exist!")
    else:
        print(f"Task failed: {result.get('error')}")

if __name__ == "__main__":
    test_passive_logging()
