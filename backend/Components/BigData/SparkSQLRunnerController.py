from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from SparkSQLRunnerHelper import run_spark_sql
from SparkSQLRunnerHelper import run_spark_sql, register_temp_view
from pyspark.sql import SparkSession
from SparkSessionManagerHelper import get_spark_session

app = FastAPI()

@app.post("/spark/sql/run")
def api_run_spark_sql(
    session_id: str = Query(...),
    query: str = Body(..., embed=True)
):
    try:
        df = run_spark_sql(session_id, query)
        if df is not None:
            return {"result": df.toJSON().collect()}
        return JSONResponse(status_code=400, content={"error": "Query failed or invalid session"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/spark/sql/register-view")
def api_register_temp_view(
    session_id: str = Query(...),
    view_name: str = Query(...),
    data: list = Body(...)
):
    try:
        session: SparkSession = get_spark_session(session_id)
        if not session:
            return JSONResponse(status_code=404, content={"error": "Session not found"})

        df = session.createDataFrame(data)
        success = register_temp_view(session_id, df, view_name)
        return {"status": "registered" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})