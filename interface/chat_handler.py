# interface/chat_handler.py

from civilization.agent_worker import AgentWorker

class ChatHandler:

    def __init__(self, civilization):
        self.civ = civilization

    def process_user_task(self, user_input):
        """
        Route human task to the civilization and return agent candidates.
        """
        candidates = []
        # We process all agents for a truly competitive hybrid result
        for agent in self.civ.agents:
            worker = AgentWorker(agent, self.civ.knowledge_pool)
            
            # Pass user_input directly to worker
            result = worker.work({
                "description": user_input,
                "reward": 20
            })
            
            # Unify output detection
            output = result.get("output") or result.get("knowledge") or result.get("data")
            if not output and result.get("success"):
                output = "Success, but no text output."
            elif not output:
                output = f"Error: {result.get('error', 'Unknown failure')}"
            
            candidates.append({
                "agent": agent.name,
                "output": str(output),
                "result_raw": result,
                "task": user_input
            })
        
        return candidates
