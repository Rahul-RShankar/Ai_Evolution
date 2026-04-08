# main.py

import os
import sys

# Add project root to sys.path for IDE and runtime resolution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from civilization.civilization_loop import Civilization
from core.multiloop_brain import MultiloopBrain

def main():
    civ = Civilization()
    brain = MultiloopBrain(civ)

    print("\n" + "="*50)
    print("🚀 AGI CIVILIZATION: AUTONOMOUS LEARNING MODE")
    print("="*50)
    print(f"Status: ONLINE")
    print(f"Goal:   Mastering Real-World Data & Coding")
    print(f"Agents: {[a.name for a in civ.agents]}")
    print("="*50 + "\n")
    
    try:
        brain.run()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Hibernating... Autonomous loop stopped.")

if __name__ == "__main__":
    main()
