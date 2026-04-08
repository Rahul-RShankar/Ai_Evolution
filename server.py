# server.py (Root Launcher)
import sys
import os

# Ensure the root is in the path for IDE and runtime resolution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface.server import app

if __name__ == "__main__":
    print("Starting AGI Civilization Backend...")
    app.run(host="0.0.0.0", port=5000)
