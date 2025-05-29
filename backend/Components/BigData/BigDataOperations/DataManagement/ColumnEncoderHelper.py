import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def label_encode_column(df: pd.DataFrame, column: str):
    try:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        return df, le
    except Exception as e:
        print(f"[ColumnEncoder] Label encoding error: {e}")
        raise

def one_hot_encode_column(df: pd.DataFrame, column: str):
    try:
        ohe_df = pd.get_dummies(df[column], prefix=column)
        df = df.drop(column, axis=1)
        df = pd.concat([df, ohe_df], axis=1)
        return df
    except Exception as e:
        print(f"[ColumnEncoder] One-hot encoding error: {e}")
        raise
