# core/meta_reflection.py

class MetaReflection:

    def analyze(self, agent):

        insights = []

        if agent.reputation < 2:
            insights.append("Improve success rate")

        if agent.energy < 50:
            insights.append("Optimize efficiency")

        return insights
