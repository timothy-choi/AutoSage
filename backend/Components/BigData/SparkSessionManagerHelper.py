from pyspark.sql import SparkSession
from typing import Dict, Optional
import uuid

_sessions: Dict[str, SparkSession] = {}


def create_spark_session(config: Optional[Dict[str, str]] = None) -> str:
    """Create a SparkSession with optional configurations."""
    session_id = str(uuid.uuid4())
    builder = SparkSession.builder.appName(f"session-{session_id}")

    if config:
        for key, value in config.items():
            builder = builder.config(key, value)

    spark = builder.getOrCreate()
    _sessions[session_id] = spark
    return session_id


def get_spark_session(session_id: str) -> Optional[SparkSession]:
    return _sessions.get(session_id)


def list_spark_sessions() -> Dict[str, str]:
    return {sid: spark.sparkContext.appName for sid, spark in _sessions.items()}


def stop_spark_session(session_id: str) -> bool:
    session = _sessions.pop(session_id, None)
    if session:
        session.stop()
        return True
    return False


def update_spark_session_config(session_id: str, config: Dict[str, str]) -> bool:
    session = _sessions.get(session_id)
    if session:
        for key, value in config.items():
            session.conf.set(key, value)
        return True
    return False