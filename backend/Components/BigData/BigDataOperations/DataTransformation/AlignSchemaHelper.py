import pandas as pd
from typing import List, Optional, Dict, Any


def align_schema(
    df: pd.DataFrame,
    schema: List[str],
    fill_value: Any = None,
    dtype_map: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    for col in schema:
        if col not in df.columns:
            df[col] = fill_value

    df = df[schema]  

    if dtype_map:
        df = df.astype(dtype_map)

    return df
