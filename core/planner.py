# core/planner.py

class Planner:

    def create_goals(self, questions):

        goals = []

        for q in questions:
            goals.append(f"Research and act on: {q}")

        return goals

    def break_into_tasks(self, goal):

        return [
            f"research {goal}",
            f"implement solution for {goal}",
            f"test solution for {goal}"
        ]
