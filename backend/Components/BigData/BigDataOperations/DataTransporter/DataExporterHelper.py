import pandas as pd
from typing import Literal

def export_data(df: pd.DataFrame, format: Literal["csv", "parquet", "json"], path: str) -> str:
    try:
        if format == "csv":
            df.to_csv(path, index=False)
        elif format == "parquet":
            df.to_parquet(path, index=False)
        elif format == "json":
            df.to_json(path, orient="records", lines=True)
        else:
            return "Unsupported format"
        return f"Data exported successfully to {path}"
    except Exception as e:
        return f"Error exporting data: {e}"