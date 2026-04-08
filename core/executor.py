import subprocess
import os
import sys
import tempfile
import importlib.util
from typing import Dict, Any, Optional
import ast
import re
from config import config

def get_dependencies(code: str, language: str) -> list:
    """Extracts top-level dependencies from code."""
    deps = []
    if language == "python":
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        deps.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    deps.append(node.module.split('.')[0])
        except SyntaxError:
            pass
    elif language in ["javascript", "node"]:
        # Find require('lib') or import 'lib' or import ... from 'lib'
        require_matches = re.findall(r"require\(['\"](.+?)['\"]\)", code)
        import_matches = re.findall(r"from\s+['\"](.+?)['\"]", code)
        deps = list(set(require_matches + import_matches))
    return list(set(deps))

def install_dependencies(deps: list, language: str):
    """Installs missing allowed dependencies."""
    if not getattr(config, "AUTO_INSTALL_DEPS", False):
        return
    
    allowed = getattr(config, "ALLOWED_LIBRARIES", [])
    for lib in deps:
        if lib in allowed:
            try:
                if language == "python":
                    # Check if already installed
                    if importlib.util.find_spec(lib) is None:
                        subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True, capture_output=True)
                elif language in ["javascript", "node"]:
                    # Install in sandbox (creates node_modules)
                    sandbox = getattr(config, "SANDBOX_DIR", "./sandbox")
                    subprocess.run(["npm", "install", lib], cwd=sandbox, check=True, capture_output=True, shell=True)
            except Exception as e:
                print(f"Failed to install {lib}: {e}")

def execute_code(code: str, language: str = "python", sandbox_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes code in various languages (python, javascript, powershell).
    """
    LANGUAGE_MAP = {
        "python": [sys.executable],
        "javascript": ["node"],
        "node": ["node"],
        "powershell": ["powershell", "-ExecutionPolicy", "Bypass", "-File"],
        "ps1": ["powershell", "-ExecutionPolicy", "Bypass", "-File"]
    }
    
    EXTENSION_MAP = {
        "python": ".py",
        "javascript": ".js",
        "node": ".js",
        "powershell": ".ps1",
        "ps1": ".ps1"
    }

    cmd_prefix = LANGUAGE_MAP.get(language.lower(), [sys.executable])
    extension = EXTENSION_MAP.get(language.lower(), ".py")
    if sandbox_dir is None:
        sandbox_dir = getattr(config, "SANDBOX_DIR", "./sandbox")
    
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    # 🛡️ SAFETY CHECK: Immediate rejection of interactive calls
    blocking_keywords = ["input(", "sys.stdin"]
    for kw in blocking_keywords:
        if kw in code:
            return {
                "output": "",
                "stdout": "",
                "stderr": f"Forbidden interactive call detected: {kw}",
                "exit_code": -1,
                "success": False,
                "error": f"Interactive calls like {kw} are forbidden in this AGI environment."
            }

    # 📦 ADM: Auto-Dependency Management
    deps = get_dependencies(code, language)
    install_dependencies(deps, language)

    with tempfile.NamedTemporaryFile(suffix=extension, dir=sandbox_dir, delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    
    timed_out = False
    try:
        process = subprocess.run(
            cmd_prefix + [tmp_path],
            capture_output=True,
            text=True,
            timeout=30  # Safety timeout
        )
        return {
            "output": process.stdout + process.stderr,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "success": process.returncode == 0,
            "error": process.stderr if process.returncode != 0 else ""
        }
    except subprocess.TimeoutExpired:
        timed_out = True
        return {
            "output": "",
            "stdout": "",
            "stderr": "Execution timed out (30s)",
            "exit_code": -1,
            "success": False,
            "error": "Execution timed out (30s)"
        }
    except Exception as e:
        return {
            "output": "",
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "success": False,
            "error": str(e)
        }
    finally:
        # Keep the file if it timed out for debugging, otherwise remove
        if os.path.exists(tmp_path) and not timed_out:
            os.remove(tmp_path)
