# core/human_learning.py

import json

class HumanLearning:

    def __init__(self, brain):
        self.brain = brain

    def categorize(self, feedback):
        """
        Determine if feedback is a reinforcement or a correction.
        """
        if feedback.get("rating") == 1:
            return "reinforce"
        elif feedback.get("correction"):
            return "corrective_learning"
        return "ignore"

    def apply_signal(self, feedback):
        """
        Route specific feedback signals to strategy and memory.
        """
        signal = self.categorize(feedback)
        
        if signal == "reinforce":
            # Direct success boost
            self.brain.strategy_engine.update("human_approved", True)
        elif signal == "corrective_learning":
            # Injects correction into priority memory
            self.brain.dataset_collector.collect(
                task=feedback["task"],
                prompt="Human Guidance",
                result=feedback["correction"],
                success=True
            )
            print(f"[HumanLearning] Strategy improved with correction: {feedback['correction'][:30]}...")

        return signal
