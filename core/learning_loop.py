import time
from agents.agent_factory import AgentFactory
from models.skill import Skill
from utils.logger import log

class LearningLoop:
    def __init__(self, queue):
        self.queue = queue

        # skill tracking
        self.skills = {
            "python": Skill("python"),
            "algorithms": Skill("algorithms")
        }

    def select_weakest_skill(self):
        return min(self.skills.values(), key=lambda s: s.score())

    def run(self):
        log("=== Autonomous Learning Loop Activated ===")
        
        while True:
            skill = self.select_weakest_skill()

            log(f"[LearningLoop] focusing on weakest skill: {skill.name} (score: {skill.score():.2f})")

            # Phase 1: Reasoning - decompose goal into tasks
            self.queue.add_task("reasoning", skill.name)

            task = self.queue.get_task()

            while task:
                log(f"[LearningLoop] Executing task: {task['type']}")
                agent = AgentFactory.create(task["type"])
                result = agent.run(task["payload"])

                log(f"[Loop Result] Result from {task['type']}: {result}")

                # route next steps based on task outcome
                if task["type"] == "reasoning":
                    # Reasoning returns a list of sub-tasks
                    for sub_task in result:
                        if "research" in sub_task.lower():
                            self.queue.add_task("research", sub_task)
                        elif "code" in sub_task.lower():
                            self.queue.add_task("coding", sub_task)

                elif task["type"] == "coding":
                    # Pass coding result to evaluation
                    self.queue.add_task("evaluation", result)

                elif task["type"] == "evaluation":
                    # Evaluate result and update skill
                    success = result.get("score", 0) > 0
                    skill.update(success)
                    log(f"[LearningLoop] Skill '{skill.name}' updated. Success: {success}, New Level: {skill.level}")

                task = self.queue.get_task()

            log("[LearningLoop] Goal cycle complete. Resting for 5 seconds...")
            time.sleep(5)
