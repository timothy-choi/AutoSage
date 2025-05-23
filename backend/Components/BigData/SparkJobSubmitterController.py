from fastapi import FastAPI, Form, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from SparkJobSubmitterHelper import submit_spark_job

app = FastAPI()

@app.post("/spark/job/submit")
def api_submit_spark_job(
    app_path: str = Form(...),
    master: str = Form("local[*]"),
    deploy_mode: str = Form("client"),
    app_args: Optional[List[str]] = Body(default=None),
    conf: Optional[Dict[str, str]] = Body(default=None),
    jars: Optional[List[str]] = Body(default=None)
):
    try:
        result = submit_spark_job(
            app_path=app_path,
            master=master,
            deploy_mode=deploy_mode,
            app_args=app_args,
            conf=conf,
            jars=jars
        )
        return {"output": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
