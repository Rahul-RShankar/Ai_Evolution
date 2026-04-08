class GoalEngine:
    def __init__(self):
        self.goals = [
            "learn python basics",
            "understand recursion",
            "build sorting algorithms"
        ]

    def get_next_goal(self):
        # simple for now (return first goal)
        return self.goals[0]
