# infra/environment.py

import requests
import subprocess
from ddgs import DDGS
from utils.logger import log

class Environment:

    def web_search(self, query, max_results=3):
        log(f"[Environment] Real Web Search (DuckDuckGo): {query}")
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=max_results)]
                return "\n\n".join([f"Source: {r['href']}\nSnippet: {r['body']}" for r in results])
        except Exception as e:
            log(f"[Environment] Search Error: {str(e)}")
            return f"Search failed for: {query}. Error: {str(e)}"

    def call_api(self, url, payload=None):
        log(f"[Environment] Calling API: {url}")
        try:
            r = requests.post(url, json=payload, timeout=5)
            return {"success": True, "data": r.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_script(self, code):
        log(f"[Environment] Running Script: {code[:30]}...")
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def act(self, action_desc):
        log(f"[Environment] Grounded Action: {action_desc}")
        return {"description": action_desc, "success": True, "data": "Grounded result simulated"}
