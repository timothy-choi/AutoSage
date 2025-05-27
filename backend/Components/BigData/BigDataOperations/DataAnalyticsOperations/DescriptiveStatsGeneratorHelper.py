import pandas as pd
from typing import Dict, Any

def generate_descriptive_stats(df: pd.DataFrame) -> Dict[str, Any]:
    stats = {}
    for col in df.columns:
        col_data = df[col]
        stats[col] = {
            "dtype": str(col_data.dtype),
            "count": int(col_data.count()),
            "nulls": int(col_data.isnull().sum()),
            "unique": int(col_data.nunique()),
        }

        if pd.api.types.is_numeric_dtype(col_data):
            stats[col].update({
                "mean": float(col_data.mean()),
                "std": float(col_data.std()),
                "min": float(col_data.min()),
                "max": float(col_data.max())
            })
    return stats
