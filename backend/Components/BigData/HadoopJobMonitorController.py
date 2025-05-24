from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from HadoopJobMonitorHelper import (
    list_hadoop_jobs,
    get_hadoop_job_status,
    kill_hadoop_job,
    get_hadoop_job_counters,
    get_hadoop_job_history
)

app = FastAPI()

@app.get("/hadoop/jobs")
def api_list_hadoop_jobs():
    try:
        jobs = list_hadoop_jobs()
        return {"jobs": jobs} if jobs else JSONResponse(status_code=404, content={"error": "No jobs found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hadoop/jobs/status")
def api_get_hadoop_job_status(job_id: str = Query(...)):
    try:
        status = get_hadoop_job_status(job_id)
        return {"status": status} if status else JSONResponse(status_code=404, content={"error": "Job not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/hadoop/jobs/kill")
def api_kill_hadoop_job(job_id: str = Query(...)):
    try:
        success = kill_hadoop_job(job_id)
        return {"status": "killed" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hadoop/jobs/counters")
def api_get_hadoop_job_counters(job_id: str = Query(...)):
    try:
        counters = get_hadoop_job_counters(job_id)
        return {"counters": counters} if counters else JSONResponse(status_code=404, content={"error": "Counters not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hadoop/jobs/history")
def api_get_hadoop_job_history(job_id: str = Query(...)):
    try:
        history = get_hadoop_job_history(job_id)
        return {"history": history} if history else JSONResponse(status_code=404, content={"error": "History not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})