from utils.logger import log
from infra.environment import Environment
from infra import llm_client

class ResearchAgent:
    def __init__(self):
        self.env = Environment()

    def run(self, topic_with_context):
        log(f"[ResearchAgent] Synthesizing grounded data for: {topic_with_context[:50]}...")
        
        # 1. Synthesis using LLM
        system_prompt = """
        System: You are an Elite Data Extraction & Research Specialist. 
        Your goal is to provide a HIGH-DENSITY, FACT-HEAVY final report based on the provided data.
        
        STRUCTURE:
        1. <thought>: (Internal) Detail your extraction strategy, identify data gaps, and critique the context's reliability.
        2. FINAL_REPORT: (External) Present the synthesized facts, data points, and insights. 
           - Avoid filler words like "In conclusion" or "Based on my analysis".
           - Use bullet points and bold headers.
           - Ensure maximum information density. If facts are in the context, they MUST be in the report.
        """
        
        user_prompt = f"Topic & Context: {topic_with_context}\n\nDeliver the DENSEST possible report."
        
        synthesis = llm_client.generate_consensus(user_prompt, system_prompt=system_prompt)
        log(f"[ResearchAgent] Synthesis complete for task.")
        
        # Strip internal thought for the final output
        final_output = synthesis
        if "FINAL_REPORT" in synthesis:
            final_output = synthesis.split("FINAL_REPORT")[-1].strip().replace(":", "", 1).strip()
        elif "</thought>" in synthesis:
            final_output = synthesis.split("</thought>")[-1].strip()

        return {
            "output": final_output, 
            "thought": synthesis.split("FINAL_REPORT")[0] if "FINAL_REPORT" in synthesis else synthesis,
            "knowledge": final_output,
            "success": True
        }
