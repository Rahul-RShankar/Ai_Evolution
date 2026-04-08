# civilization/agent_profile.py

from civilization.identity import Identity

class AgentProfile:

    def __init__(self, name):
        self.name = name
        self.energy = 100
        self.reputation = 0
        self.skills = {
            "coding": 1,
            "research": 1
        }
        self.identity = Identity(name)

    def improve(self, skill):
        self.skills[skill] = self.skills.get(skill, 0) + 1

    def __repr__(self):
        return f"{self.name} | Energy: {self.energy} | Rep: {self.reputation}"
