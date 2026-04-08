# civilization/economy.py

class Economy:

    def __init__(self):
        self.balances = {}

    def reward(self, agent_name, amount):
        self.balances[agent_name] = self.balances.get(agent_name, 0) + amount

    def get_balance(self, agent_name):
        return self.balances.get(agent_name, 0)
