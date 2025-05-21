from fastapi import FastAPI, Form, Query
from fastapi.responses import JSONResponse
from FileSystemManagerHelper import *

app = FastAPI()

@app.post("/fs/copy-dir")
def api_copy_directory(src: str = Form(...), dst: str = Form(...)):
    try:
        copy_directory(src, dst)
        return {"status": "directory copied"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/is-dir")
def api_is_directory(path: str = Query(...)):
    try:
        return {"is_directory": is_directory(path)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/is-file")
def api_is_file(path: str = Query(...)):
    try:
        return {"is_file": is_file(path)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/exists")
def api_path_exists(path: str = Query(...)):
    try:
        return {"exists": path_exists(path)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/metadata")
def api_get_metadata(path: str = Query(...)):
    try:
        meta = get_metadata(path)
        return {"metadata": meta} if meta else JSONResponse(status_code=404, content={"error": "Path not found or inaccessible."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/list")
def api_list_directory(path: str = Query(...)):
    try:
        return {"contents": list_directory(path)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/fs/create-dir")
def api_create_directory(path: str = Form(...)):
    try:
        create_directory(path)
        return {"status": "directory created"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/fs/delete-file")
def api_delete_file(path: str = Query(...)):
    try:
        delete_file(path)
        return {"status": "file deleted"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/fs/delete-dir")
def api_delete_directory(path: str = Query(...)):
    try:
        delete_directory(path)
        return {"status": "directory deleted"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/fs/move")
def api_move_file(src: str = Form(...), dst: str = Form(...)):
    try:
        move_file(src, dst)
        return {"status": "moved"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/fs/copy")
def api_copy_file(src: str = Form(...), dst: str = Form(...)):
    try:
        copy_file(src, dst)
        return {"status": "copied"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/size")
def api_get_file_size(path: str = Query(...)):
    try:
        size = get_file_size(path)
        return {"size_bytes": size}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/fs/abs")
def api_get_absolute_path(path: str = Query(...)):
    try:
        abs_path = get_absolute_path(path)
        return {"absolute_path": abs_path}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/fs/rename")
def api_rename_path(src: str = Form(...), dst: str = Form(...)):
    try:
        rename_path(src, dst)
        return {"status": "renamed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})