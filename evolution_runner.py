# evolution_runner.py

from infra.self_evolution import evolution_manager
import sys

def main():
    print("=== AI Evolution Manager ===")
    print("Action: Active Learning Cycle (Expert Iteration)")
    print("Source: action_memory.json (Failures/Invalidations)")
    print("Target: training_data.jsonl")
    print("-----------------------------------")
    
    confirm = input("Start learning cycle now? (y/n): ")
    if confirm.lower() == 'y':
        evolution_manager.run_learning_cycle()
        print("\nCycle complete. Check training_data.jsonl for new expert examples.")
    else:
        print("Cycle cancelled.")

if __name__ == "__main__":
    main()
