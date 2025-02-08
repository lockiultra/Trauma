from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
DATASET_ROOT = PROJECT_ROOT / 'data/'
FAISS_DB_ROOT = PROJECT_ROOT / 'data/faiss'


print(FAISS_DB_ROOT)