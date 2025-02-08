import faiss
from config.data import HF_DATASET
from config.paths import FAISS_DB_ROOT, DATASET_ROOT
from config.models import SENTENCE_MODEL
from sentence_transformers import SentenceTransformer
from datasets import load_dataset


def encode_contexts():
    # dataset = load_dataset(DATASET_ROOT / 'dataset')
    dataset = load_dataset(HF_DATASET)
    contexts = dataset['train']['content']
    model = SentenceTransformer(SENTENCE_MODEL)
    vectors = model.encode(contexts, show_progress_bar=True)
    return vectors


def create_faiss_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(vectors)
    print(f'Количество записей в индексе: {index.ntotal}')

    faiss.write_index(FAISS_DB_ROOT / 'faiss_index.index')


if __name__ == '__main__':
    vectors = encode_contexts()
    create_faiss_index(vectors)
