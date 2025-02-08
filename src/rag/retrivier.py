import os
import faiss
import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from config.paths import FAISS_DB_ROOT
from config.data import HF_DATASET


class Retrivier:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = FAISS_DB_ROOT / 'faiss_index.index'
        self.dataset = load_dataset(HF_DATASET)['train']
        self.index = self.__load_faiss_index()

    def __load_faiss_index(self):
        index = faiss.read_index(str(self.index_path))
        return index

    async def get_context(self, question: str, top_k: int = 3) -> str:
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        question_embedding = self.model.encode(question)
        question_embedding = np.expand_dims(question_embedding, axis=0)
        distances, indices = self.index.search(question_embedding, top_k)
        contexts = [self.dataset[index]['content'] for index in indices]
        return '\n'.join(contexts[0])
