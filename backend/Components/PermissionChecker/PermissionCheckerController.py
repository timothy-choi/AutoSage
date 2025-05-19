from fastapi import FastAPI, Query
from PermissionCheckerHelper import *

app = FastAPI()

@app.get("/permissions")
def api_check_permissions(path: str = Query(...)):
    try:
        return check_permissions(path)
    except Exception as e:
        return {"error": str(e)}

@app.get("/permissions/mode")
def api_get_mode(path: str = Query(...)):
    try:
        return {"mode": get_file_mode(path)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/permissions/owner")
def api_get_owner(path: str = Query(...)):
    try:
        return get_file_owner(path)
    except Exception as e:
        return {"error": str(e)}

@app.get("/permissions/symlink")
def api_is_symlink(path: str = Query(...)):
    try:
        return {"is_symlink": is_symlink(path)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/permissions/symlink-target")
def api_symlink_target(path: str = Query(...)):
    try:
        return {"target": get_symlink_target(path)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/permissions/size")
def api_get_file_size(path: str = Query(...)):
    try:
        return {"size_bytes": get_file_size(path)}
    except Exception as e:
        return {"error": str(e)}