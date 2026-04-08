# civilization/knowledge_pool.py

class KnowledgePool:

    def __init__(self):
        self.data = []

    def add(self, knowledge):
        self.data.append(knowledge)

    def get_recent(self, k=3):
        return self.data[-k:]
