import heapq
import time
from typing import List, Dict, Any, Optional

class Task:
    def __init__(self, description: str, priority: int = 1, metadata: Optional[Dict] = None):
        self.description = description
        self.priority = priority  # Lower number = higher priority
        self.metadata = metadata or {}
        self.timestamp = time.time()
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result: Any = None

    def __lt__(self, other):
        # Tie-breaker using timestamp if priority is equal
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority < other.priority

class TaskQueue:
    def __init__(self):
        self.queue: List[Task] = []
        self.history: List[Task] = []

    def add_task(self, description: str, priority: int = 1, metadata: Optional[Dict] = None) -> Task:
        task = Task(description, priority, metadata)
        heapq.heappush(self.queue, task)
        return task

    def get_next_task(self) -> Optional[Task]:
        if not self.queue:
            return None
        task = heapq.heappop(self.queue)
        task.status = "in_progress"
        return task

    def complete_task(self, task: Task, result: Any):
        task.status = "completed"
        task.result = result
        self.history.append(task)

    def fail_task(self, task: Task, error: str):
        task.status = "failed"
        task.result = error
        self.history.append(task)

    def get_pending_count(self) -> int:
        return len(self.queue)

if __name__ == "__main__":
    tq = TaskQueue()
    tq.add_task("Learn about quantum computing", priority=2)
    tq.add_task("Fix broken code executor", priority=1)
    
    print(f"Pending tasks: {tq.get_pending_count()}")
    next_task = tq.get_next_task()
    if next_task:
        print(f"Working on: {next_task.description} (Priority: {next_task.priority})")
