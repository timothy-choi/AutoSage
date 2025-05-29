import pandas as pd
import dask.dataframe as dd

def join_large_dataframes(df1_path, df2_path, join_column, how='inner', use_dask=False):
    try:
        if use_dask:
            df1 = dd.read_csv(df1_path)
            df2 = dd.read_csv(df2_path)
            joined = df1.merge(df2, on=join_column, how=how)
            return joined.compute()
        else:
            df1 = pd.read_csv(df1_path)
            df2 = pd.read_csv(df2_path)
            return df1.merge(df2, on=join_column, how=how)
    except Exception as e:
        print(f"[BigJoiner] Join error: {e}")
        raise
