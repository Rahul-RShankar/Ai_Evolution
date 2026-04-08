# core/self_model.py

import json
import os

class SelfModel:

    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.goals = []
        self.skills = {}
        self.history = []
        self.lessons_learned = []
        self.current_focus = None
        self._load()

    def update(self, result):
        self.history.append(result)
        # Limit history size
        if len(self.history) > 20:
            self.history.pop(0)
        self.save()

    def add_lesson(self, lesson):
        if lesson not in self.lessons_learned:
            self.lessons_learned.append(lesson)
            # Max 10 most critical lessons
            if len(self.lessons_learned) > 10:
                self.lessons_learned.pop(0)
            self.save()

    def reflect(self):
        insights = []
        
        # Simple reflection logic
        success_rate = self._get_success_rate()
        
        if success_rate < 0.5:
            insights.append("Change strategy - current effectiveness is low")
        
        # Check for repetitive tasks or patterns
        if len(self.history) >= 5:
            tasks = [h.get("description", "") for h in self.history[-5:]]
            if len(set(tasks)) < 3:
                insights.append("Explore new domain - repetition detected")

        return insights

    def _get_success_rate(self):
        if not self.history:
            return 1.0
        successes = [h for h in self.history if h.get("success")]
        return len(successes) / len(self.history)

    def save(self):
        filepath = f"{self.agent_name}_self_model.json"
        data = {
            "goals": self.goals,
            "skills": self.skills,
            "history": self.history,
            "lessons_learned": self.lessons_learned,
            "current_focus": self.current_focus
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def _load(self):
        filepath = f"{self.agent_name}_self_model.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    self.goals = data.get("goals", [])
                    self.skills = data.get("skills", {})
                    self.history = data.get("history", [])
                    self.lessons_learned = data.get("lessons_learned", [])
                    self.current_focus = data.get("current_focus")
            except Exception:
                pass
