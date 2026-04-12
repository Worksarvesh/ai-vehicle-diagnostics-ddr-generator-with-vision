import pandas as pd
from pathlib import Path


def load_csv_data(path: str) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    return pd.read_csv(dataset_path)
