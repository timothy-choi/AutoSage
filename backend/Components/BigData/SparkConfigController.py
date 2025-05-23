from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from SparkConfigHelper import (
    write_spark_defaults,
    read_spark_defaults,
    write_spark_env,
    read_spark_env
)
from typing import Dict

app = FastAPI()

@app.post("/spark/defaults/write")
def api_write_spark_defaults(properties: Dict[str, str] = Body(...)):
    try:
        write_spark_defaults(properties)
        return {"status": "spark-defaults.conf updated"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/defaults/read")
def api_read_spark_defaults():
    try:
        return {"properties": read_spark_defaults()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/spark/env/write")
def api_write_spark_env(vars: Dict[str, str] = Body(...)):
    try:
        write_spark_env(vars)
        return {"status": "spark-env.sh updated"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/env/read")
def api_read_spark_env():
    try:
        return {"env_vars": read_spark_env()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})