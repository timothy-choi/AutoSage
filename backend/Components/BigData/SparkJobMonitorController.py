from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from SparkJobMonitorHelper import (
    list_spark_jobs,
    get_job_details,
    list_spark_stages,
    list_spark_executors
)

app = FastAPI()

@app.get("/spark/jobs")
def api_list_spark_jobs():
    try:
        jobs = list_spark_jobs()
        return {"jobs": jobs} if jobs is not None else JSONResponse(status_code=404, content={"error": "Unable to retrieve jobs"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/jobs/{job_id}")
def api_get_job_details(job_id: int):
    try:
        job = get_job_details(job_id)
        return {"job": job} if job is not None else JSONResponse(status_code=404, content={"error": f"Job {job_id} not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/stages")
def api_list_spark_stages():
    try:
        stages = list_spark_stages()
        return {"stages": stages} if stages is not None else JSONResponse(status_code=404, content={"error": "Unable to retrieve stages"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/executors")
def api_list_spark_executors():
    try:
        executors = list_spark_executors()
        return {"executors": executors} if executors is not None else JSONResponse(status_code=404, content={"error": "Unable to retrieve executors"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
