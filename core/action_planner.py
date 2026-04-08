# core/action_planner.py

class ActionPlanner:

    def decide(self, task):
        task_lower = task.lower()

        if "search" in task_lower or "lookup" in task_lower:
            return ("web_search", task)

        if "api" in task_lower or "endpoint" in task_lower:
            # Mock endpoint for now
            return ("call_api", {"url": "https://api.intelligence.org/feedback"})

        if "code" in task_lower or "script" in task_lower or "execute" in task_lower:
            # Extract code if present, or simulate
            return ("run_script", "print('Autonomous script execution success')")

        return ("none", None)
