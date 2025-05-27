import pandas as pd
from typing import Dict, Any, List, Union

def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    for col, val in filters.items():
        if col in df.columns:
            df = df[df[col] == val]
    return df

def filter_with_conditions(df: pd.DataFrame, conditions: List[Dict[str, Union[str, Any]]]) -> pd.DataFrame:
    for cond in conditions:
        col = cond.get("column")
        op = cond.get("operator")
        val = cond.get("value")

        if col not in df.columns:
            continue

        if op == "==":
            df = df[df[col] == val]
        elif op == "!=":
            df = df[df[col] != val]
        elif op == ">":
            df = df[df[col] > val]
        elif op == "<":
            df = df[df[col] < val]
        elif op == ">=":
            df = df[df[col] >= val]
        elif op == "< =":
            df = df[df[col] <= val]
        elif op == "in" and isinstance(val, list):
            df = df[df[col].isin(val)]
    return df