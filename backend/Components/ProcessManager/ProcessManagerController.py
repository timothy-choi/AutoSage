from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ProcessManagerController import (
    list_processes,
    get_process_details,
    terminate_process,
    kill_process
)

router = APIRouter()

class PIDRequest(BaseModel):
    pid: int

@router.get("/processes")
def list_all_processes():
    result = list_processes()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/processes/{pid}")
def get_details(pid: int):
    result = get_process_details(pid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/processes/terminate")
def terminate(data: PIDRequest):
    result = terminate_process(data.pid)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/processes/kill")
def kill(data: PIDRequest):
    result = kill_process(data.pid)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result