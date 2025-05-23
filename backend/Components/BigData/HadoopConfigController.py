from fastapi import FastAPI, Form, Query, Body
from fastapi.responses import JSONResponse
from typing import Dict
from HadoopConfigHelper import write_hadoop_config, read_hadoop_config, format_namenode

app = FastAPI()

@app.post("/hadoop/config/write")
def api_write_hadoop_config(
    file_name: str = Form(...),
    properties: Dict[str, str] = Body(...)
):
    try:
        write_hadoop_config(file_name, properties)
        return {"status": f"Configuration written to {file_name}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/hadoop/config/read")
def api_read_hadoop_config(file_name: str = Query(...)):
    try:
        config = read_hadoop_config(file_name)
        return {"file": file_name, "properties": config}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/hadoop/format")
def api_format_namenode(hdfs_dir: str = Form("/tmp/hdfs/namenode")):
    try:
        success = format_namenode(hdfs_dir)
        return {"status": "success" if success else "failure"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})