from utils.logger import log

class GoalGenerator:
    def generate(self, memory):
        # In a real system, this would analyze memory to find gaps
        # For now, return a list of strategic goals
        goals = [
            {"type": "research", "payload": "advanced sorting algorithms", "reward": 20},
            {"type": "coding", "payload": "implement quicksort in python", "reward": 50},
            {"type": "research", "payload": "distributed systems basics", "reward": 30}
        ]
        log(f"[GoalGenerator] Generated {len(goals)} new strategic goals")
        return goals

class CuriosityEngine:
    def __init__(self):
        self.questions = [
            "What do I not understand?",
            "Where did I fail recently?",
            "What skill is weakest right now?"
        ]

    def detect_gaps(self, agent_profile):
        # Simple gap detection based on skills with low success rates
        gaps = []
        for skill_name, stats in agent_profile.skills.items():
            if stats["level"] < 2 or stats["success"] / stats["attempts"] < 0.5:
                gaps.append(f"missing mastery in {skill_name}")
        
        if not gaps:
            gaps.append("expanding into new territory")
        
        return gaps
