import pandas as pd
import numpy as np
from typing import Dict


def analyze_correlation(data: pd.DataFrame) -> Dict[str, float]:
    try:
        corr_matrix = data.corr()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        correlated_pairs = {
            f"{col1} & {col2}": round(upper.loc[col1, col2], 4)
            for col1 in upper.columns for col2 in upper.index
            if not pd.isna(upper.loc[col1, col2]) and abs(upper.loc[col1, col2]) > 0.5
        }
        return correlated_pairs
    except Exception as e:
        return {"error": str(e)}
