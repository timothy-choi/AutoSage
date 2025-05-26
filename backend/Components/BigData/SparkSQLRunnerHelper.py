from typing import Optional
from pyspark.sql import DataFrame
from SparkSessionManagerHelper import get_spark_session


def run_spark_sql(session_id: str, query: str) -> Optional[DataFrame]:
    """
    Run a SQL query in the context of the given SparkSession.
    """
    session = get_spark_session(session_id)
    if session:
        try:
            return session.sql(query)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    return None


def register_temp_view(session_id: str, df: DataFrame, view_name: str) -> bool:
    """
    Register a DataFrame as a temporary SQL view in the Spark session.
    """
    session = get_spark_session(session_id)
    if session:
        try:
            df.createOrReplaceTempView(view_name)
            return True
        except Exception as e:
            print(f"Error creating view: {e}")
            return False
    return False