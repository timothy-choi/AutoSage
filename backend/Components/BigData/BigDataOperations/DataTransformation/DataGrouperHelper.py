import pandas as pd
from typing import List, Dict, Optional


def group_and_aggregate(
    df: pd.DataFrame,
    group_by: List[str],
    aggregations: Dict[str, str],
    dropna: Optional[bool] = True
) -> pd.DataFrame:
    if dropna:
        df = df.dropna(subset=group_by)

    grouped = df.groupby(group_by).agg(aggregations).reset_index()
    return grouped
