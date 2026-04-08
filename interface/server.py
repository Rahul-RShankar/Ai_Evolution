# interface/server.py

from flask import Flask, request, jsonify
import json
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# Ensure root is in path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Core Global Instances
try:
    from civilization.civilization_loop import Civilization
    from core.multiloop_brain import MultiloopBrain
    from interface.chat_handler import ChatHandler
    from core.feedback_processor import FeedbackProcessor
    
    civ = Civilization()
    brain = MultiloopBrain(civ)
    chat_handler = ChatHandler(civ)
    feedback_processor = FeedbackProcessor(brain.strategy_engine, brain.dataset_collector)
except Exception as e:
    print(f"CRITICAL: Failed to initialize AGI Core: {str(e)}")
    civ = None # Handle missing core gracefully if possible

MEMORY_FILE = "human_feedback.json"

def save_feedback(data):
    try:
        with open(MEMORY_FILE, "r") as f:
            existing = json.load(f)
    except:
        existing = []
    existing.append(data)
    with open(MEMORY_FILE, "w") as f:
        json.dump(existing, f, indent=2)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"error": "No message provided"}), 400
            
        if not chat_handler:
            return jsonify({"error": "Chat handler not initialized"}), 503
            
        # Route to multi-agent competition
        candidates = chat_handler.process_user_task(user_msg)
        return jsonify({"candidates": candidates})
    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return jsonify({"error": str(e), "status": 500}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    # data format: { agent_name, task, result_raw, rating, correction, intent }
    
    agent_name = data.get("agent_name")
    task = data.get("task")
    result_raw = data.get("result_raw")
    rating = data.get("rating")
    correction = data.get("correction")
    
    # Process through intelligence engine
    feedback_processor.process_feedback(
        agent_name, task, result_raw, rating, correction
    )
    
    save_feedback(data)
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
