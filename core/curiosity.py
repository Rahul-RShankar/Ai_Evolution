# core/curiosity.py

from infra import llm_client
import json

class CuriosityEngine:

    def generate_questions(self, agent, mission="General Improvement"):
        """
        Dynamically generate curiosity questions using LLM based on mission and agent state.
        """
        # Get context from agent (history, skills, lessons)
        history_snippet = [h.get("description", "") for h in agent.history[-5:]] if hasattr(agent, "history") else []
        skills_snippet = agent.skills if hasattr(agent, "skills") else {}
        lessons_snippet = agent.lessons_learned if hasattr(agent, "lessons_learned") else []

        prompt = f"""
        System: You are the Curiosity Engine of an autonomous AGI.
        Goal: Generate 3 diverse, high-value tasks that expand the AGI's knowledge or skills.
        
        AGI Mission: {mission}
        Recent History: {history_snippet}
        Current Skills: {skills_snippet}
        Lessons Learned: {lessons_snippet}
        
        Requirements:
        1. One task must be RESEARCH-based (finding new data).
        2. One task must be CODING-based (building a tool or automation).
        3. One task must be REFLECTIVE/OPTIMIZATION-based (improving current logic).
        
        Return exactly 3 strings in a JSON list format: ["task1", "task2", "task3"]
        """

        try:
            response = llm_client.generate(prompt)
            # Find JSON list
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end != -1:
                questions = json.loads(response[start:end])
                return questions
        except Exception as e:
            print(f"[Curiosity] Failed to generate dynamic questions: {e}")
        
        # Fallback to a single generic question based on mission
        return [f"Research latest developments related to {mission}"]
