# civilization/civilization_loop.py

import time
import random

from civilization.agent_profile import AgentProfile
from civilization.economy import Economy
from civilization.market import TaskMarket
from civilization.agent_worker import AgentWorker
from civilization.knowledge_pool import KnowledgePool
from civilization.competition import Competition


class Civilization:

    def __init__(self):

        self.agents = [
            AgentProfile("Agent_A"), # Will be our Master Coder
            AgentProfile("Agent_B"), # Will be our Strategic Researcher
            AgentProfile("Agent_C")
        ]

        self.economy = Economy()
        self.market = TaskMarket()
        self.knowledge_pool = KnowledgePool()
        self.competition = Competition()

    def run(self):

        self.market.seed_tasks()

        while True:

            print("\n--- Civilization Cycle ---")

            task = self.market.get_task()

            if not task:
                continue

            print(f"\nTarget Task: {task['description']}")

            results = {}

            # All agents compete on SAME task
            for agent_profile in self.agents:

                worker = AgentWorker(agent_profile, self.knowledge_pool)

                result = worker.work(task)

                results[agent_profile.name] = result

                print(f"{agent_profile.name} result success: {result.get('success', False)}")

            # Evaluate winner
            winner, score = self.competition.evaluate(results)

            print(f"\nWinner: {winner}")

            # reward winner
            if winner:
                self.economy.reward(winner, task["reward"])

                for agent in self.agents:
                    if agent.name == winner:
                        agent.reputation += 2
                        agent.improve("coding")

            # Knowledge sharing
            for result in results.values():
                if result.get("success"):
                    self.knowledge_pool.add(result)

            # Leaderboard
            print("\nLeaderboard:")
            for agent in self.agents:
                balance = self.economy.get_balance(agent.name)
                print(f"{agent.name} | Balance: {balance} | Rep: {agent.reputation}")

            # Loop waits for next task from market
            time.sleep(2)

            time.sleep(5)
