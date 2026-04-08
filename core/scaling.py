# core/scaling.py

class ScalingManager:

    def __init__(self):
        self.max_agents = 10

    def should_spawn(self, performance_score):
        # Spawn if success rate/performance is high
        return performance_score > 0.8

    def spawn_agent(self, agents_list, agent_profile_class):

        if len(agents_list) < self.max_agents:
            new_name = f"Agent_{chr(65 + len(agents_list))}" # Agent_D, E, etc.
            new_agent = agent_profile_class(new_name)
            agents_list.append(new_agent)
            return new_agent
        
        return None
