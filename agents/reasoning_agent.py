from utils.logger import log

class ReasoningAgent:
    def run(self, goal):
        log(f"[ReasoningAgent] analyzing goal: {goal}")

        # naive decomposition (upgrade later with LLM)
        tasks = [
            f"research {goal}",
            f"write code for {goal}",
            f"test implementation of {goal}"
        ]

        return tasks
