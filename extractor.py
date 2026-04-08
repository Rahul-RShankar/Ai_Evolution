import json
from typing import Dict, Any, List

# Import config safely to satisfy strict linter
try:
    import config # type: ignore
    sys_config = config.config
except (ImportError, AttributeError):
    # This should only happen if run in an environment where config.py isn't found
    class MockConfig:
        MODEL_NAME = "gpt-4-turbo"
    sys_config = MockConfig()

class KnowledgeExtractor:
    """
    Distills raw text/data into structured 'Knowledge Objects'.
    """
    def __init__(self, client=None):
        self.client = client

    def extract(self, raw_data: str, context: str = "") -> List[Dict[str, Any]]:
        """
        Uses LLM to extract facts from raw data.
        """
        raw_data_str: str = str(raw_data)
        if not self.client:
            # Using slice in a way that should satisfy the most stubborn linters
            summary = raw_data_str[0:100] # type: ignore
            return [{"key": "Raw Info", "value": summary, "confidence": 0.1}]

        # Using explicit string formatting and slicing to avoid linter errors
        context_data = raw_data_str[0:2000] # type: ignore
        prompt = f"""
        Extract key facts from the following data.
        Context: {context}
        Data: {context_data}
        
        Return a list of JSON objects: [{{"key": "...", "value": "...", "confidence": 0.0-1.0}}]
        """

        try:
            response = self.client.chat.completions.create(
                model=sys_config.MODEL_NAME,
                messages=[{"role": "system", "content": "You are a precise knowledge extractor."},
                          {"role": "user", "content": prompt}]
            )
            # Basic parsing of the response content for JSON list
            content: str = str(response.choices[0].message.content)
            # Locate first '[' and last ']'
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != -1:
                json_part = content[start:end] # type: ignore
                return json.loads(json_part)
            return []
        except Exception as e:
            print(f"Extraction error: {e}")
            return []

if __name__ == "__main__":
    extractor = KnowledgeExtractor()
    print(extractor.extract("Python 3.12 was released recently with improvements in speed."))
