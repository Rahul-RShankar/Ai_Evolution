# core/strategy_engine.py

class StrategyEngine:

    def __init__(self):
        self.strategies = {
            "direct_code": {"success": 0, "attempts": 0},
            "research_then_code": {"success": 0, "attempts": 0}
        }

    def choose(self):

        # pick best success rate
        best = max(
            self.strategies,
            key=lambda s: (
                self.strategies[s]["success"] /
                (self.strategies[s]["attempts"] + 1)
            )
        )

        return best

    def update(self, strategy, success):

        self.strategies[strategy]["attempts"] += 1

        if success:
            self.strategies[strategy]["success"] += 1
