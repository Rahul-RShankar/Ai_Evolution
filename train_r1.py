# train_r1.py
from infra.self_evolution import evolution_manager
from utils.logger import log

def main():
    log("[TrainR1] Starting Automated Expert Reflection Cycle...")
    print("=== DeepSeek-R1 Training Phase ===")
    print("Target: action_memory.json (Failures/Invalidations)")
    print("Model: deepseek-r1:14b (Local)")
    print("-----------------------------------")
    
    evolution_manager.run_learning_cycle()
    
    print("\n[SUCCESS] Reflection cycle complete.")
    print("Check training_data.jsonl for new expert demonstrations.")

if __name__ == "__main__":
    main()
