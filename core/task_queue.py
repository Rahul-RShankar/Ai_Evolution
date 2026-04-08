from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task_type, payload):
        self.queue.append({
            "type": task_type,
            "payload": payload
        })

    def get_task(self):
        if self.queue:
            return self.queue.popleft()
        return None
