# core/feedback_processor.py

class FeedbackProcessor:

    def __init__(self, strategy_engine, dataset_collector):
        self.strategy_engine = strategy_engine
        self.dataset_collector = dataset_collector

    def process_feedback(self, agent_name, task, result_raw, rating, correction=None):
        """
        Apply human reinforcement to the agent's strategy and memory.
        """
        success = (rating == 1)
        
        # 1. Update Strategy Engine with human truth
        # ...
        
        # 2. Update Persistent Memory
        from memory.memory_store import MemoryStore
        mem = MemoryStore()
        if not success:
            # If rejected, kill the confidence of the original memory
            mem.invalidate(task)
            print(f"[Feedback] Data for '{task[:20]}...' has been INVALIDATED in memory.")
        
        # 3. Record human-verified data
        verified_record = {
            "task": task,
            "output": correction if correction else result_raw,
            "success": success,
            "confidence": 1.0 if success else 0.0,
            "verified": success,
            "source": "Human Correction" if correction else "Human Approval"
        }
        mem.save(verified_record)

        self.dataset_collector.collect(
            task=task,
            prompt=f"Human Feedback: {correction}" if correction else "Human Recommended Output",
            result=correction if correction else result_raw,
            success=success
        )

        print(f"[Feedback] Human Rating for {agent_name}: {'POSITIVE' if success else 'NEGATIVE'}")
        if correction:
            print(f"[Feedback] Correction Received: {correction[:30]}...")
        
        return success
