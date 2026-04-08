# core/priority_filter.py

class PriorityFilter:

    @staticmethod
    def is_valuable(task):
        """
        Filter tasks based on keywords that signal high intelligence value.
        """
        keywords = ["coding", "automation", "strategy", "optimization", "ethics", "business"]
        task_lower = task.lower()
        
        # High value if it contains a keyword
        return any(k in task_lower for k in keywords)

    @staticmethod
    def get_priority(task):
        """
        Return a priority score (1-10) for a task.
        """
        if "coding" in task.lower():
            return 10
        if "automation" in task.lower():
            return 8
        return 5
