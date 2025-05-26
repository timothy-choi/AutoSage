from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from SparkSQLRunnerHelper import run_spark_sql

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