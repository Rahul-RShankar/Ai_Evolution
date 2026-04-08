from agents.coding_agent import CodingAgent
from agents.research_agent import ResearchAgent
from agents.evaluation_agent import EvaluationAgent
from agents.reasoning_agent import ReasoningAgent

class AgentFactory:
    registry = {
        "coding": CodingAgent,
        "research": ResearchAgent,
        "evaluation": EvaluationAgent,
        "reasoning": ReasoningAgent
    }

    @classmethod
    def create(cls, agent_type):
        agent_class = cls.registry.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return agent_class()
