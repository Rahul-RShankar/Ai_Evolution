# hitl_runner.py

from civilization.civilization_loop import Civilization
from core.multiloop_brain import MultiloopBrain
from interface.web_app import HumanInterface

def main():
    civ = Civilization()
    brain = MultiloopBrain(civ)
    
    # Initialize the Human Interface with the active brain
    interface = HumanInterface(civ, brain)
    
    print("Starting AGI Civilization with Human-in-the-Loop...")
    
    interface.run()

if __name__ == "__main__":
    main()
