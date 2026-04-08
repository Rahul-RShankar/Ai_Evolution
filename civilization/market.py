# civilization/market.py

import random

class TaskMarket:

    def __init__(self):
        self.tasks = []

    def post_task(self, description, reward):
        self.tasks.append({
            "description": description,
            "reward": reward
        })

    def get_task(self):
        if not self.tasks:
            return None
        return self.tasks.pop(0)

    def seed_tasks(self):
        base_tasks = [
            "write python function for factorial",
            "explain recursion with example",
            "build fibonacci program"
        ]

        for task in base_tasks:
            self.post_task(task, reward=random.randint(5, 15))
