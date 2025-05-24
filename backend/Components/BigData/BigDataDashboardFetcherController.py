from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from BigDataDashboardFetcherHelper import (
    fetch_yarn_cluster_metrics,
    fetch_yarn_apps,
    fetch_spark_applications,
    fetch_spark_environment
)

app = FastAPI()

@app.get("/dashboard/yarn/metrics")
def api_yarn_cluster_metrics():
    try:
        metrics = fetch_yarn_cluster_metrics()
        return {"metrics": metrics} if metrics else JSONResponse(status_code=404, content={"error": "YARN metrics not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/dashboard/yarn/apps")
def api_yarn_apps(state: str = Query("RUNNING")):
    try:
        apps = fetch_yarn_apps(state)
        return {"apps": apps} if apps else JSONResponse(status_code=404, content={"error": "No YARN apps found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/dashboard/spark/apps")
def api_spark_apps():
    try:
        apps = fetch_spark_applications()
        return {"apps": apps} if apps else JSONResponse(status_code=404, content={"error": "No Spark apps found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/dashboard/spark/environment")
def api_spark_environment(app_id: str = Query(...)):
    try:
        env = fetch_spark_environment(app_id)
        return {"environment": env} if env else JSONResponse(status_code=404, content={"error": "Spark environment not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})