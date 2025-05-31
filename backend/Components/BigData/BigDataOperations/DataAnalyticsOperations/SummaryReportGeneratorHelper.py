import pandas as pd

def generate_numeric_summary(df: pd.DataFrame) -> dict:
    summary = df.describe(include="number").to_dict()
    return summary

def generate_textual_summary(df: pd.DataFrame) -> dict:
    summary = {}
    for col in df.select_dtypes(include="object").columns:
        summary[col] = {
            "unique_count": df[col].nunique(),
            "top_values": df[col].value_counts().head(5).to_dict()
        }
    return summary

def generate_full_summary(df: pd.DataFrame) -> dict:
    return {
        "numeric_summary": generate_numeric_summary(df),
        "textual_summary": generate_textual_summary(df)
    }