from utils.logger import log

class TaskMarket:
    def __init__(self):
        self.jobs = []

    def post_job(self, task_type, payload, reward):
        job = {
            "type": task_type,
            "payload": payload,
            "reward": reward,
            "status": "open"
        }
        self.jobs.append(job)
        log(f"[Market] New job posted: {task_type} (Reward: {reward} tokens)")

    def get_open_jobs(self):
        return [job for job in self.jobs if job["status"] == "open"]

    def acquire_job(self, agent_name):
        open_jobs = self.get_open_jobs()
        if not open_jobs:
            return None
        
        # For now, pick the first open job. (Bidding logic can be added later)
        job = open_jobs[0]
        job["status"] = "in-progress"
        job["assignee"] = agent_name
        log(f"[Market] Job '{job['type']}' acquired by {agent_name}")
        return job

    def complete_job(self, job):
        job["status"] = "completed"
        log(f"[Market] Job '{job['type']}' completed by {job.get('assignee')}")
