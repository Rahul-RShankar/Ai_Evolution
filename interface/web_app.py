# interface/web_app.py

import sys
from interface.chat_handler import ChatHandler
from core.feedback_processor import FeedbackProcessor

class HumanInterface:

    def __init__(self, civ, multiloop_brain):
        self.handler = ChatHandler(civ)
        self.feedback = FeedbackProcessor(
            multiloop_brain.strategy_engine, 
            multiloop_brain.dataset_collector
        )

    def run(self):
        print("\n=== AGI CIVILIZATION HUMAN CONTROL PANEL ===")
        print("Commands: [task] <your_task> | [exit]")
        
        while True:
            u_input = input("\nHuman Control > ").strip()
            if u_input.lower() == "exit":
                break
            
            if u_input.startswith("task "):
                task = u_input[5:]
                print(f"\n[Injecting Task]: {task}")
                candidates = self.handler.process_user_task(task)
                
                print("\n--- AGENT CANDIDATE RESPONSES ---")
                for i, c in enumerate(candidates):
                    print(f"[{i}] {c['agent']}: {c['output'][:100]}...")
                
                # Evaluation UI
                choice = input("\nSelect best agent [0-2], rate [1/0], or input correction: ").strip()
                
                if choice.isdigit() and int(choice) in range(len(candidates)):
                    selected = candidates[int(choice)]
                    # Auto-positive rating for selected
                    self.feedback.process_feedback(
                        selected['agent'], 
                        task, 
                        selected['result_raw'], 
                        1
                    )
                else:
                    # Treat as correction for all if text input
                    for c in candidates:
                        self.feedback.process_feedback(
                            c['agent'], 
                            task, 
                            c['result_raw'], 
                            0, 
                            correction=choice
                        )

if __name__ == "__main__":
    # Integration note: This would be launched alongside main.py
    pass
