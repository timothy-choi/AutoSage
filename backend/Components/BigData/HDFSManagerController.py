from fastapi import FastAPI, Form, Query
from fastapi.responses import JSONResponse
from HDFSManagerHelper import (
    hdfs_put,
    hdfs_get,
    hdfs_mkdir,
    hdfs_rm,
    hdfs_ls,
    hdfs_cat
)

app = FastAPI()

@app.post("/hdfs/put")
def api_hdfs_put(local_path: str = Form(...), hdfs_path: str = Form(...)):
    try:
        success = hdfs_put(local_path, hdfs_path)
        return {"status": "uploaded" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/hdfs/get")
def api_hdfs_get(hdfs_path: str = Form(...), local_path: str = Form(...)):
    try:
        success = hdfs_get(hdfs_path, local_path)
        return {"status": "downloaded" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/hdfs/mkdir")
def api_hdfs_mkdir(hdfs_path: str = Form(...)):
    try:
        success = hdfs_mkdir(hdfs_path)
        return {"status": "created" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/hdfs/rm")
def api_hdfs_rm(path: str = Query(...), recursive: bool = Query(False)):
    try:
        success = hdfs_rm(path, recursive)
        return {"status": "deleted" if success else "failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hdfs/ls")
def api_hdfs_ls(path: str = Query(...)):
    try:
        result = hdfs_ls(path)
        return {"contents": result} if result is not None else JSONResponse(status_code=404, content={"error": "not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hdfs/cat")
def api_hdfs_cat(path: str = Query(...)):
    try:
        content = hdfs_cat(path)
        return {"content": content} if content is not None else JSONResponse(status_code=404, content={"error": "file not found or empty"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})