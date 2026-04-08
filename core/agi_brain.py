# core/agi_brain.py

import time
import random

from core.curiosity import CuriosityEngine
from core.deep_planner import DeepPlanner
from core.meta_reflection import MetaReflection
from core.memory_weighting import WeightedMemory
from core.strategy_engine import StrategyEngine
from core.self_modifier import SelfModifier
from core.hybrid_reasoner import HybridReasoner
from core.scaling import ScalingManager

from civilization.agent_worker import AgentWorker
from civilization.protocol import Message
from civilization.agent_profile import AgentProfile

from infra.llm_client import generate


class AGIBrain:

    def __init__(self, civilization):

        self.civ = civilization

        self.curiosity = CuriosityEngine()
        self.planner = DeepPlanner()
        self.meta = MetaReflection()
        self.memory = WeightedMemory()
        self.strategy_engine = StrategyEngine()
        self.self_modifier = SelfModifier()
        self.hybrid_reasoner = HybridReasoner()
        self.scaling_manager = ScalingManager()

        self.message_bus = [] # Global message room for collaboration

    def run(self):

        while True:

            print("\n--- FINAL AGI MASTER LOOP ---")

            for agent in self.civ.agents:

                print(f"\n{agent.name} (Identity: {agent.identity.traits}) is thinking...")

                # 1. Curiosity Goal Generation
                questions = self.curiosity.generate_questions(agent)

                for question in questions:
                    
                    # 2. Hybrid Reasoning (Symbolic + Neural)
                    # Use LLM client for neural part
                    logical_plan = self.hybrid_reasoner.solve(question, generate)
                    print(f"Hybrid Reasoner output: {logical_plan}")

                    # 3. Strategy Selection
                    strategy = self.strategy_engine.choose()

                    # 4. Planning
                    plan = self.planner.plan(logical_plan)
                    
                    completed_steps = {}
                    worker = AgentWorker(agent, self.civ.knowledge_pool)

                    for step in plan:
                        if step["depends_on"] is None or completed_steps.get(step["depends_on"], False):
                            
                            # Retrieve context from weighted memory
                            context = self.memory.retrieve()
                            
                            # Check message bus for help if curious or stuck
                            if agent.identity.traits["curiosity"] > 0.8:
                                recent_help = [m.to_dict() for m in self.message_bus[-3:]]
                                context.append({"type": "communication", "history": recent_help})

                            result = worker.work({
                                "description": f"{step['task']} | Context: {context}",
                                "reward": 10
                            })

                            success = result.get("success", False)
                            completed_steps[step["step"]] = success

                            # Evolution & Memory
                            self.strategy_engine.update(strategy, success)
                            self.memory.add(result, success)
                            agent.identity.evolve(success)

                            if success:
                                agent.improve("coding")
                                agent.reputation += 1
                                self.civ.economy.reward(agent.name, 5)
                                self.civ.knowledge_pool.add(result)
                            else:
                                # Self-Modification & Communication
                                print(f"{agent.name} failed step. Requesting help...")
                                
                                # Collaborative Messaging
                                help_msg = Message(
                                    sender=agent.name,
                                    receiver="all",
                                    intent="request_help",
                                    content=f"Failed task: {step['task']}"
                                )
                                self.message_bus.append(help_msg)

                                # Attempt self-fix
                                improved = self.self_modifier.improve_code(str(result), "failed")
                                print(f"Self-Fix Attempt: {improved[:30]}...")

                # 5. Meta Reflection
                insights = self.meta.analyze(agent)
                print(f"Reflection: {insights}")

                # 6. Scaling (Spawning new agents)
                # Performance score based on reputation/reception
                perf = min(1.0, agent.reputation / 100.0 + 0.5) 
                if self.scaling_manager.should_spawn(perf):
                    new_agent = self.scaling_manager.spawn_agent(self.civ.agents, AgentProfile)
                    if new_agent:
                        print(f"PERFORMANCE THRESHOLD MET: Spawned {new_agent.name}")

            # State summary
            print("\nCivilization State:")
            for agent in self.civ.agents:
                balance = self.civ.economy.get_balance(agent.name)
                print(f"{agent.name} | Balance: {balance} | Traits: {agent.identity.traits}")

            time.sleep(5)
