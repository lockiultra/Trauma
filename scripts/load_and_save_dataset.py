from config.data import HF_DATASET
from config.paths import DATASET_ROOT
from datasets import load_dataset


def load_and_save_dataset():
    dataset = load_dataset(HF_DATASET)
    dataset.save_to_disk(DATASET_ROOT / 'dataset')


if __name__ == '__main__':
    load_and_save_dataset()
