import pandas as pd
import os
from typing import Optional


def import_dataset(
    path: str,
    file_type: str = "csv",
    delimiter: str = ",",
    encoding: Optional[str] = "utf-8"
) -> pd.DataFrame:
    """Load dataset from local file or remote storage (e.g., S3)."""
    if file_type == "csv":
        return pd.read_csv(path, delimiter=delimiter, encoding=encoding)
    elif file_type == "json":
        return pd.read_json(path, encoding=encoding)
    elif file_type == "parquet":
        return pd.read_parquet(path)
    elif file_type == "excel":
        return pd.read_excel(path)
    elif file_type == "avro":
        import fastavro
        with open(path, 'rb') as f:
            reader = fastavro.reader(f)
            return pd.DataFrame(list(reader))
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
