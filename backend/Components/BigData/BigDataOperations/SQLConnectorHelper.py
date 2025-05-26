import sqlalchemy
from sqlalchemy import text
from typing import Optional, List, Dict, Any

_supported_drivers = {
    "postgresql": "postgresql://{user}:{password}@{host}:{port}/{database}",
    "mysql": "mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
    "sqlite": "sqlite:///{database}"
}


def build_connection_url(
    driver: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    database: Optional[str] = None
) -> Optional[str]:
    if driver not in _supported_drivers:
        return None
    return _supported_drivers[driver].format(
        user=user or "",
        password=password or "",
        host=host or "localhost",
        port=port or "5432",
        database=database or ""
    )


def run_sql_query(url: str, query: str) -> List[Dict[str, Any]]:
    engine = sqlalchemy.create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = [dict(row._mapping) for row in result]
    return rows


def list_tables(url: str) -> List[str]:
    engine = sqlalchemy.create_engine(url)
    inspector = sqlalchemy.inspect(engine)
    return inspector.get_table_names()


def get_table_schema(url: str, table_name: str) -> List[Dict[str, Any]]:
    engine = sqlalchemy.create_engine(url)
    inspector = sqlalchemy.inspect(engine)
    columns = inspector.get_columns(table_name)
    return columns