from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from SparkContextManagerHelper import (
    get_spark_context_status,
    stop_spark_context,
    get_active_rdd_names
)

app = FastAPI()

@app.get("/spark/context/status")
def api_get_spark_context_status(session_id: str = Query(...)):
    try:
        status = get_spark_context_status(session_id)
        return {"context": status} if status else JSONResponse(status_code=404, content={"error": "Session not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/spark/context/stop")
def api_stop_spark_context(session_id: str = Query(...)):
    try:
        stopped = stop_spark_context(session_id)
        return {"status": "stopped" if stopped else "not found or already stopped"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/context/rdds")
def api_get_active_rdds(session_id: str = Query(...)):
    try:
        rdds = get_active_rdd_names(session_id)
        return {"rdds": rdds} if rdds is not None else JSONResponse(status_code=404, content={"error": "Session not found or no RDDs"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})