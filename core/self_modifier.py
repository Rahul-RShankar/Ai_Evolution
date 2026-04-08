# core/self_modifier.py

from infra.llm_client import generate

class SelfModifier:

    def improve_code(self, code, feedback):

        prompt = f"""
Improve this code based on feedback.

CODE:
{code}

FEEDBACK:
{feedback}

Return improved version only.
"""

        improved = generate(prompt)

        return improved
