from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from typing import Optional, Dict
from SQLConnectorHelper import (
    build_connection_url,
    run_sql_query,
    list_tables,
    get_table_schema
)

app = FastAPI()

@app.post("/sql/query")
def api_run_sql_query(
    driver: str = Query(...),
    user: Optional[str] = Query(None),
    password: Optional[str] = Query(None),
    host: Optional[str] = Query("localhost"),
    port: Optional[str] = Query("5432"),
    database: Optional[str] = Query(None),
    query: str = Body(..., embed=True)
):
    try:
        url = build_connection_url(driver, user, password, host, port, database)
        if not url:
            return JSONResponse(status_code=400, content={"error": "Unsupported driver"})
        result = run_sql_query(url, query)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/sql/tables")
def api_list_tables(
    driver: str = Query(...),
    user: Optional[str] = Query(None),
    password: Optional[str] = Query(None),
    host: Optional[str] = Query("localhost"),
    port: Optional[str] = Query("5432"),
    database: Optional[str] = Query(None)
):
    try:
        url = build_connection_url(driver, user, password, host, port, database)
        if not url:
            return JSONResponse(status_code=400, content={"error": "Unsupported driver"})
        tables = list_tables(url)
        return {"tables": tables}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/sql/schema")
def api_get_table_schema(
    driver: str = Query(...),
    user: Optional[str] = Query(None),
    password: Optional[str] = Query(None),
    host: Optional[str] = Query("localhost"),
    port: Optional[str] = Query("5432"),
    database: Optional[str] = Query(None),
    table_name: str = Query(...)
):
    try:
        url = build_connection_url(driver, user, password, host, port, database)
        if not url:
            return JSONResponse(status_code=400, content={"error": "Unsupported driver"})
        schema = get_table_schema(url, table_name)
        return {"schema": schema}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})