from utils.logger import log

class EvaluationAgent:
    def run(self, result):
        log("[EvaluationAgent] evaluating result")

        # Basic scoring logic
        success = result.get("success", False)
        score = 1 if success else 0

        return {
            "score": score,
            "feedback": "Good" if score else "Needs improvement",
            "success": success
        }
