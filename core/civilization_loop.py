import time
from core.economy import Economy
from core.market import TaskMarket
from agents.intelligence import GoalGenerator, CuriosityEngine
from agents.agent_factory import AgentFactory
from models.agent_profile import AgentProfile
from memory.vector_store import VectorStore
from utils.logger import log

class CivilizationLoop:
    def __init__(self):
        self.economy = Economy()
        self.market = TaskMarket()
        self.goal_generator = GoalGenerator()
        self.curiosity = CuriosityEngine()
        self.memory = VectorStore()
        
        # Initialize a population of specialized agents
        self.agents = [
            AgentProfile("Alpha", "research_expert"),
            AgentProfile("Beta", "coding_expert"),
            AgentProfile("Gamma", "evaluation_expert")
        ]
        
        # Register them in economy
        for agent in self.agents:
            self.economy.register_agent(agent.name)

    def run(self):
        log("=== AI Civilization Loop Started ===")
        
        cycle = 1
        while True:
            log(f"\n--- Civilization Cycle {cycle} ---")
            
            # 1. Goal Generation (The collective brain decides what's important)
            strategic_goals = self.goal_generator.generate(self.memory)
            for goal in strategic_goals:
                self.market.post_job(goal["type"], goal["payload"], goal["reward"])

            # 2. Agent Action (Agents compete/collaborate to acquire jobs)
            for agent_profile in self.agents:
                # Agent check: Do we have energy?
                if agent_profile.energy < 10:
                    log(f"[Civilization] Agent {agent_profile.name} is resting...")
                    agent_profile.rest()
                    continue

                # 3. Market Participation
                job = self.market.acquire_job(agent_profile.name)
                if job:
                    # Create the actual agent worker
                    worker = AgentFactory.create(job["type"])
                    
                    # Execute the work
                    result = worker.run(job["payload"])
                    log(f"[Civilization] Agent {agent_profile.name} finished {job['type']}. Result: {result.get('success', False)}")

                    # 4. Evaluation and Reward (Simplified evaluation for now)
                    # In Phase 5, another agent would typically evaluate
                    success = result.get("success", False)
                    if success:
                        self.economy.reward(agent_profile.name, job["reward"])
                        agent_profile.reputation += 1
                        # Learn: Save to shared vector memory
                        self.memory.add(f"Task: {job['payload']} | Result: {result}")
                    
                    agent_profile.update_skill(job["type"], success)
                    self.market.complete_job(job)

            # 5. Reflection Cycle
            log("\n--- Civilization State ---")
            for agent in self.agents:
                log(f"Agent {agent.name}: Tokens={self.economy.get_balance(agent.name)}, Skills={agent.skills}")

            cycle += 1
            log(f"Cycle {cycle} complete. Cooling down for 5 seconds...")
            time.sleep(5)
