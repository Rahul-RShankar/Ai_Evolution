from core.executor import execute_code
from config import config
from utils.logger import log
from memory.memory_store import MemoryStore
from infra import llm_client

MAX_FIX_ATTEMPTS = getattr(config, "MAX_FIX_ATTEMPTS", 3)
memory = MemoryStore()

class CodingAgent:
    def run(self, task: str):
        log(f"[CodingAgent] Starting real task: {task}")

        # 🔍 STEP 1: CHECK MEMORY
        past = memory.search(task)

        context = ""
        if past:
            log("[CodingAgent] Using past knowledge")
            context = f"Previous similar solutions:\n{past}\n"

        system_prompt = """
        System: You are an Elite Polyglot Programmer. 
        Your goal is to provide a correct, efficient, and robust solution in Python, JavaScript, or PowerShell.
        
        STRUCTURE:
        1. <thought>: (Internal) Detail your logic, language choice, and risk mitigation.
        2. SELF-CRITIQUE: (Internal) Identify 2-3 risks and explain your mitigation strategy.
        3. CODE: (External) Return ONLY valid code in a markdown block.
        
        CRITICAL: NEVER use `input()` or interactive blocking calls.
        """
        
        user_prompt = f"{context}\nTask: {task}\n\nDeliver the most robust code possible."
        
        consensus_result = llm_client.generate_consensus(user_prompt, system_prompt=system_prompt)
        
        # Handle dict or string (fallback)
        if isinstance(consensus_result, dict):
            raw_response = consensus_result.get("winner", "")
            reasoning = consensus_result.get("reasoning", "No reasoning provided.")
        else:
            raw_response = consensus_result
            reasoning = "N/A (Direct Generation)"

        log(f"[CodingAgent] Judge Reasoning: {reasoning}")
        
        # 🛡️ SAFETY CHECK: DO NOT execute if it's an error message
        if not raw_response or raw_response.startswith("ERROR:"):
            error_msg = raw_response or "Empty response"
            log(f"[CodingAgent] Aborting: LLM returned error: {error_msg}")
            return {
                "success": False,
                "output": f"LLM Failure: {error_msg}",
                "error": error_msg
            }

        # 🧹 CLEAN & DETECT LANGUAGE
        language = "python"  # Default
        lang_options = ["python", "javascript", "node", "powershell", "ps1"]
        code = raw_response
        
        if "```" in raw_response:
            parts = raw_response.split("```")
            if len(parts) > 1:
                content = parts[1]
                # Detect language from tag
                first_line = content.split('\n')[0].strip().lower()
                if any(l in first_line for l in lang_options):
                    language = first_line
                    code = content[len(first_line):].strip()
                else:
                    code = content.strip()
        
        attempt = 0
        while attempt < MAX_FIX_ATTEMPTS:
            result = execute_code(code, language=language)

            # ✅ SUCCESS
            if result.get("success"):
                # Safety check: Ensure the response actually looks like code
                code_str = str(code)
                if not any(keyword in code_str for keyword in ["import", "def", "print", "=", "function", "var", "const", "let"]):
                     log(f"[CodingAgent] WARNING: Non-code output detected. Skipping success.")
                     attempt += 1
                     continue
                
                log("[CodingAgent] Execution successful")
                
                # 🧬 SELF-EVOLUTION: Log success for training
                from infra.self_evolution import evolution_manager
                evolution_manager.log_success(task, code)

                memory.save({
                    "task": task,
                    "code": code,
                    "output": result.get("output", ""),
                    "success": True
                })

                clean_output = f"**Execution Output:**\n{result.get('output', '')}"
                raw_response_str = str(raw_response)
                return {
                    "output": clean_output,
                    "thought": raw_response_str.split("```")[0] if "```" in raw_response_str else "",
                    "success": True,
                    "code": code_str,
                    "execution_output": result.get("output")
                }

            # ❌ FAILURE
            log(f"[CodingAgent] Error: {result.get('error')}")

            memory.save({
                "task": task,
                "code": code,
                "error": result.get("error"),
                "success": False
            })

            fix_prompt = f"""
            System: Fix this {language} code. Return ONLY valid code in a markdown block.
            
            Previous attempts: {past}
            
            CODE WITH ERROR:
            {code}
            
            STDOUT/STDERR:
            {result.get('error')}
            
            Fixed Code:
            """

            raw_fix_result = llm_client.generate_consensus(fix_prompt)
            
            if isinstance(raw_fix_result, dict):
                raw_fix = raw_fix_result.get("winner", "")
            else:
                raw_fix = raw_fix_result
                
            if "```" in str(raw_fix):
                parts = str(raw_fix).split("```")
                if len(parts) > 1:
                    content = parts[1]
                    first_line = content.split('\n')[0].strip().lower()
                    if any(l in first_line for l in lang_options):
                        code = content[len(first_line):].strip()
                    else:
                        code = content.strip()
            else:
                code = str(raw_fix).strip()
            
            attempt += 1

        return {
            "success": False,
            "output": "",
            "error": "Max attempts reached"
        }
