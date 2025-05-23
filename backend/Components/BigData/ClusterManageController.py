from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ClusterManageHelper import (
    start_namenode, stop_namenode,
    start_datanode, stop_datanode,
    start_resourcemanager, stop_resourcemanager,
    start_nodemanager, stop_nodemanager,
    start_spark_master, stop_spark_master,
    start_spark_worker, stop_spark_worker
)

app = FastAPI()

@app.post("/cluster/hadoop/namenode/start")
def api_start_namenode():
    try:
        return {"status": "started"} if start_namenode() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/hadoop/namenode/stop")
def api_stop_namenode():
    try:
        return {"status": "stopped"} if stop_namenode() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/hadoop/datanode/start")
def api_start_datanode():
    try:
        return {"status": "started"} if start_datanode() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/hadoop/datanode/stop")
def api_stop_datanode():
    try:
        return {"status": "stopped"} if stop_datanode() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/yarn/resourcemanager/start")
def api_start_resourcemanager():
    try:
        return {"status": "started"} if start_resourcemanager() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/yarn/resourcemanager/stop")
def api_stop_resourcemanager():
    try:
        return {"status": "stopped"} if stop_resourcemanager() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/yarn/nodemanager/start")
def api_start_nodemanager():
    try:
        return {"status": "started"} if start_nodemanager() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/yarn/nodemanager/stop")
def api_stop_nodemanager():
    try:
        return {"status": "stopped"} if stop_nodemanager() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/master/start")
def api_start_spark_master():
    try:
        return {"status": "started"} if start_spark_master() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/master/stop")
def api_stop_spark_master():
    try:
        return {"status": "stopped"} if stop_spark_master() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/worker/start")
def api_start_spark_worker():
    try:
        return {"status": "started"} if start_spark_worker() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/cluster/spark/worker/stop")
def api_stop_spark_worker():
    try:
        return {"status": "stopped"} if stop_spark_worker() else {"status": "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})