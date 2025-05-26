import pandas as pd
from typing import List, Dict, Optional


def map_columns(
    df: pd.DataFrame,
    rename_map: Optional[Dict[str, str]] = None,
    drop_columns: Optional[List[str]] = None,
    reorder_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Applies column renaming, dropping, and reordering to a DataFrame.
    """
    if rename_map:
        df = df.rename(columns=rename_map)

    if drop_columns:
        df = df.drop(columns=[col for col in drop_columns if col in df.columns])

    if reorder_columns:
        reordered = [col for col in reorder_columns if col in df.columns]
        remaining = [col for col in df.columns if col not in reordered]
        df = df[reordered + remaining]

    return df