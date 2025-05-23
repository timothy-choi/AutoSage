from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from ClusterLauncherHelper import (
    start_hadoop_cluster,
    stop_hadoop_cluster,
    start_spark_cluster,
    stop_spark_cluster,
    run_command
)

app = FastAPI()

@app.post("/cluster/hadoop/start")
def api_start_hadoop():
    try:
        success = start_hadoop_cluster()
        return {"status": "started" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/hadoop/stop")
def api_stop_hadoop():
    try:
        success = stop_hadoop_cluster()
        return {"status": "stopped" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/start")
def api_start_spark():
    try:
        success = start_spark_cluster()
        return {"status": "started" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/stop")
def api_stop_spark():
    try:
        success = stop_spark_cluster()
        return {"status": "stopped" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/cluster/command")
def api_run_command(cmd: str = Query(...)):
    try:
        output = run_command(cmd)
        return {"output": output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})