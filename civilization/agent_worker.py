from agents.agent_factory import AgentFactory
from infra.environment import Environment
from core.self_model import SelfModel
from infra import llm_client
from utils.logger import log

class AgentWorker:

    def __init__(self, profile, knowledge_pool):
        self.profile = profile
        self.knowledge_pool = knowledge_pool
        self.env = Environment()
        self.self_model = SelfModel(profile.name)

    def reflect_on_failure(self, task_desc, error_output):
        log(f"[AgentWorker] Reflecting on failure for: {self.profile.name}")
        
        reflection_prompt = f"""
        System: You are an AGI Meta-Learner analyzing a technical failure.
        Your goal is to extract a PRECISE technical rule to prevent this specific error in the future.
        
        CRITICAL: 
        1. DO NOT generalize the failure to the entire task (e.g., do NOT say "Never print tables").
        2. DO identify specific forbidden patterns (e.g., "Always avoid `input()`", "Never use non-whitelisted libraries").
        3. If the error mentions 'input(' being forbidden, the rule MUST be about using hardcoded values or `sys.argv`.
        4. If it's a `ModuleNotFoundError`, the rule MUST be about checking the whitelist or using Standard Library.
        
        Task: {task_desc}
        Error: {error_output}
        
        Format: "Never [specific code pattern] because [technical reason]" OR "Always [specific pattern] to avoid [technical error]"
        Rule:
        """
        lesson = llm_client.generate_consensus(reflection_prompt).strip()
        
        # Post-process: Take only the first line and strip common filler
        clean_lesson = lesson.split('\n')[0].replace("#", "").replace("**", "").strip()
        if clean_lesson and "ERROR" not in clean_lesson:
            self.self_model.add_lesson(clean_lesson)
            log(f"[AgentWorker] New Lesson Learned: {clean_lesson}")

    def work(self, task):
        task_desc = task['description']
        log(f"[AgentWorker] Orchestrating Search-First for: {task_desc}")

        # 1. 🔍 SEARCH FIRST: Always ground in the real world
        search_query = task_desc
        search_results = self.env.web_search(search_query, max_results=3)

        # 2. 🧠 MEMORY: Retrieve recent collective knowledge AND self-lessons
        local_context = self.knowledge_pool.get_recent(k=2)
        my_lessons = "\n".join([f"- {l}" for l in self.self_model.lessons_learned])
        
        # 3. 🛡️ CURATE: Combine for the worker
        enriched_context = f"--- REAL-WORLD DATA ---\n{search_results}\n\n--- LOCAL KNOWLEDGE ---\n{local_context}\n\n--- LESSONS LEARNT ---\n{my_lessons}"

        description_lower = task_desc.lower()
        # Strict Intent Detection - Prioritize Informational
        research_indicators = ["tell me about", "what is", "define", "explain", "who is", "why", "difference between", "research"]
        coding_indicators = ["write a", "create a", "build a", "implement", "fix a", "code for", "script", "app", "function", "javascript", "node", "powershell", "ps1"]
        
        is_research_intent = any(kw in description_lower for kw in research_indicators)
        is_coding_intent = any(kw in description_lower for kw in coding_indicators)
        
        # Priority: Explicit Coding intent first, then Research
        if is_coding_intent:
            agent = AgentFactory.create("coding")
        elif is_research_intent:
            agent = AgentFactory.create("research")
        else:
            # Default to research if no clear intent, or the agent's best skill
            if self.profile.skills.get("coding", 0) > self.profile.skills.get("research", 0):
                agent = AgentFactory.create("coding")
            else:
                agent = AgentFactory.create("research")

        # Pass the unified grounded prompt
        result = agent.run(f"{task_desc} | GROUNDED CONTEXT: {enriched_context}")
        
        # 4. 🔄 AUTO-LEARN: Reflect on failure
        if not result.get("success", False):
            error_info = result.get("error", "") or result.get("output", "")
            self.reflect_on_failure(task_desc, error_info)
            
        # Log internal thought for transparency
        if result.get("thought"):
            log(f"[AgentWorker] {self.profile.name} Internal Thought:\n{result['thought'][:500]}...")

        # Update self-model history
        current_output = str(result.get("output", ""))
        self.self_model.update({
            "description": task_desc,
            "success": result.get("success", False),
            "output_snippet": current_output[:100]
        })
        
        return result
