import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        # Using a small, efficient model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Dimension for all-MiniLM-L6-v2 is 384
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype('float32'))
        self.texts.append(text)

    def search(self, query, k=3):
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)

        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.texts):
                results.append(self.texts[i])
        return results
