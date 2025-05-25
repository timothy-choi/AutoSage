from pyspark import SparkContext
from typing import Optional, Dict
from SparkSessionManagerHelper import get_spark_session


def get_spark_context_status(session_id: str) -> Optional[Dict[str, str]]:
    session = get_spark_session(session_id)
    if not session:
        return None
    sc: SparkContext = session.sparkContext
    return {
        "appName": sc.appName,
        "master": sc.master,
        "sparkUser": sc.sparkUser(),
        "isStopped": str(sc._jsc.sc().isStopped())
    }


def stop_spark_context(session_id: str) -> bool:
    session = get_spark_session(session_id)
    if session:
        sc = session.sparkContext
        if not sc._jsc.sc().isStopped():
            sc.stop()
            return True
    return False


def get_active_rdd_names(session_id: str) -> Optional[list]:
    session = get_spark_session(session_id)
    if session:
        return [rdd.name() for rdd in session.sparkContext._jsc.sc().getPersistentRDDs().values()]
    return None