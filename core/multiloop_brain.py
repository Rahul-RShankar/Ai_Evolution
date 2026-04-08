# core/multiloop_brain.py

import time
import random

from core.curiosity import CuriosityEngine
from core.deep_planner import DeepPlanner
from core.self_model import SelfModel
from core.world_model import WorldModel
from core.strategy_engine import StrategyEngine
from core.self_modifier import SelfModifier
from core.hybrid_reasoner import HybridReasoner
from core.action_planner import ActionPlanner
from core.dataset_collector import DatasetCollector
from core.trust_scoring import TrustScoring
from core.priority_filter import PriorityFilter

from infra.environment import Environment
from civilization.agent_worker import AgentWorker


class MultiloopBrain:

    def __init__(self, civilization):
        self.civ = civilization
        
        self.curiosity = CuriosityEngine()
        self.planner = DeepPlanner()
        self.strategy_engine = StrategyEngine()
        self.self_modifier = SelfModifier()
        self.hybrid_reasoner = HybridReasoner()
        self.world_model = WorldModel()
        self.env = Environment()
        self.action_planner = ActionPlanner()
        self.dataset_collector = DatasetCollector()
        self.trust_scoring = TrustScoring()
        self.priority_filter = PriorityFilter()
        
        # Initialize self-models for each agent
        self.self_models = {agent.name: SelfModel(agent.name) for agent in self.civ.agents}

    def run_step(self, agent):
        """
        Execute a single thinking/acting cycle for a specific agent.
        """
        MISSION = "Research current AI trends and generate strategic reports"
        self_model = self.self_models[agent.name]
        
        # --- 1. EVOLUTION LOOP ---
        insights = self_model.reflect()
        
        # --- 2. LEARNING LOOP ---
        # Generate curiosity questions based on the mission
        questions = self.curiosity.generate_questions(agent, mission=MISSION)
        
        for question in questions:
            # We enforce the REAL WORLD MISSION here
            if not self.priority_filter.is_valuable(question):
                # If curiosity is too generic, nudge it towards the mission
                question = f"Research latest developments in {MISSION}"
                
            print(f"\n[MISSION CONTROL] {agent.name} is pursuing: {question}")
            
            # Execute the question as a task
            self.execute_task_sequence(agent, question, MISSION)

    def execute_task_sequence(self, agent, task_desc, mission):
        """Logic for executing a task and checking for follow-up actions."""
        plan_instruction = self.hybrid_reasoner.solve(task_desc, lambda x: f"LLM thought: {x}", self.env)
        strategy = self.strategy_engine.choose()
        plan = self.planner.plan(plan_instruction)
        
        completed_steps = {}
        worker = AgentWorker(agent, self.civ.knowledge_pool)
        self_model = self.self_models[agent.name]

        for step in plan:
            if step["depends_on"] is None or completed_steps.get(step["depends_on"], False):
                action, payload = self.action_planner.decide(step["task"])
                
                # Execution logic (Search, API, Script, or AgentWork)
                if action == "web_search":
                    result = {"description": step["task"], "success": True, "data": self.env.web_search(payload)}
                elif action == "call_api":
                    result = self.env.call_api(payload["url"])
                    result["description"] = step["task"]
                elif action == "run_script":
                    result = self.env.run_script(payload)
                    result["description"] = step["task"]
                else:
                    result = worker.work({"description": step["task"], "reward": 10})

                success = result.get("success", False)
                completed_steps[step["step"]] = success

                # Collect and update models
                self.dataset_collector.collect(task=step["task"], prompt=plan_instruction, result=result, success=success)
                self_model.update(result)
                self.strategy_engine.update(strategy, success)
                
                if not success:
                    print(f"[REPAIR] Attempting to fix failed step: {step['task']}")
                    improved_action = self.self_modifier.improve_code(str(result), "Fix the failure and try again.")
                    # In a real system, we'd parse and re-execute. 
                    # For now, we log the attempt and move to reflection.
                    self_model.add_lesson(f"Failed {step['task']}: {result.get('error')}")

        # --- 4. TASK CHAINING (Reflection) ---
        self.reflect_and_chain(agent, task_desc, mission)

    def reflect_and_chain(self, agent, completed_task, mission):
        """Ask the LLM if a follow-up task is needed based on the previous result."""
        self_model = self.self_models[agent.name]
        history = [h.get("description", "") for h in self_model.history[-3:]]
        
        prompt = f"""
        System: You are the Strategic Reflection module of an autonomous AGI.
        A task has just been completed. Decide if a follow-up task is necessary.
        
        Mission: {mission}
        Completed Task: {completed_task}
        Recent History: {history}
        
        If a follow-up is needed (e.g. implementing what was researched, or debugging what failed), return the description of the NEXT TASK.
        If no immediate follow-up is needed, return "DONE".
        
        Return exactly the task description or "DONE".
        """
        
        try:
            from infra import llm_client
            next_task = llm_client.generate(prompt).strip()
            if next_task != "DONE" and len(next_task) > 5:
                print(f"[RE-CHAIN] {agent.name} proposed follow-up: {next_task}")
                # Depth-limited recursion (1 level) to avoid infinite loops without progress
                # For real autonomy, we'd add it to a proper queue
                self.execute_task_sequence(agent, next_task, mission)
        except Exception as e:
            print(f"[Reflection] Chaining failed: {e}")

    def run(self):
        while True:
            print("\n--- [PRODUCTION] HYBRID INTELLIGENCE MULTILOOP CYCLE ---")
            for agent in self.civ.agents:
                try:
                    self.run_step(agent)
                except Exception as e:
                    print(f"[CRITICAL ERROR] Loop failure for {agent.name}: {str(e)}")
            time.sleep(10)
