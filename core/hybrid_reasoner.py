# core/hybrid_reasoner.py

class HybridReasoner:

    def __init__(self):
        self.rules = {
            "factorial": "n! = n * (n-1)!",
            "fibonacci": "f(n)=f(n-1)+f(n-2)"
        }

    def symbolic_reason(self, problem):

        for key in self.rules:
            if key in problem.lower():
                return f"Use rule: {self.rules[key]}"

        return None

    def neural_reason(self, problem, llm_func):
        # llm_func is expected to be a function that takes a string and returns a string
        return llm_func(problem)

    def solve(self, problem, llm_func, environment=None):

        # 1. Symbolic Match (Rules/Math)
        symbolic = self.symbolic_reason(problem)
        if symbolic:
            return f"{symbolic}"

        # 2. Tool-First / Grounded execution check
        if environment and ("api" in problem.lower() or "real-world" in problem.lower() or "data" in problem.lower()):
            # Fallback to direct environment action if task implies grounded tool usage
            return f"Use Environment: {problem}"

        # 3. Neural Fallback (LLM)
        return self.neural_reason(problem, llm_func)
