from fastapi import FastAPI, Form, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional, Dict
from SparkSessionManagerHelper import (
    create_spark_session,
    get_spark_session,
    list_spark_sessions,
    stop_spark_session,
    update_spark_session_config
)

app = FastAPI()

@app.post("/spark/session/create")
def api_create_spark_session(config: Optional[Dict[str, str]] = Body(default=None)):
    try:
        session_id = create_spark_session(config)
        return {"session_id": session_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/session/list")
def api_list_spark_sessions():
    try:
        sessions = list_spark_sessions()
        return {"sessions": sessions}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/session/get")
def api_get_spark_session(session_id: str = Query(...)):
    try:
        session = get_spark_session(session_id)
        if session:
            return {"session_id": session_id, "app_name": session.sparkContext.appName}
        return JSONResponse(status_code=404, content={"error": "Session not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/spark/session/stop")
def api_stop_spark_session(session_id: str = Query(...)):
    try:
        success = stop_spark_session(session_id)
        return {"status": "stopped" if success else "not found"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.put("/spark/session/update")
def api_update_spark_session_config(
    session_id: str = Query(...),
    config: Dict[str, str] = Body(...)
):
    try:
        success = update_spark_session_config(session_id, config)
        return {"status": "updated" if success else "not found"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})