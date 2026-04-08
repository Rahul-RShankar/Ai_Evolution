from utils.logger import log

class Economy:
    def __init__(self, initial_wealth=100):
        self.balances = {}
        self.initial_wealth = initial_wealth

    def register_agent(self, agent_name):
        if agent_name not in self.balances:
            self.balances[agent_name] = self.initial_wealth
            log(f"[Economy] Registered {agent_name} with {self.initial_wealth} tokens")

    def reward(self, agent_name, amount):
        if agent_name not in self.balances:
            self.register_agent(agent_name)
        self.balances[agent_name] += amount
        log(f"[Economy] Rewarded {agent_name} with {amount} tokens. New balance: {self.balances[agent_name]}")

    def spend(self, agent_name, amount) -> bool:
        if agent_name not in self.balances:
            self.register_agent(agent_name)
        
        if self.balances[agent_name] >= amount:
            self.balances[agent_name] -= amount
            log(f"[Economy] {agent_name} spent {amount} tokens. Remaining: {self.balances[agent_name]}")
            return True
        else:
            log(f"[Economy] {agent_name} has insufficient funds ({self.balances[agent_name]}) for amount {amount}")
            return False

    def get_balance(self, agent_name):
        return self.balances.get(agent_name, 0)
