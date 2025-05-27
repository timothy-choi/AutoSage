import pandas as pd
from typing import Optional, Any

def normalize_datetime_column(
    df: pd.DataFrame,
    column: str,
    input_format: Optional[str] = None,
    output_format: Optional[str] = None,
    errors: str = "coerce"
) -> pd.DataFrame:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], format=input_format, errors=errors)
        if output_format:
            df[column] = df[column].dt.strftime(output_format)
    return df