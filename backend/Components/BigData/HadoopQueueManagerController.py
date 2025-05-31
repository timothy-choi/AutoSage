from fastapi import APIRouter, HTTPException
from HadoopQueueManagerHelper import list_queues, get_queue_info, get_raw_scheduler_info

router = APIRouter()

@router.get("/hadoop/queues")
def list_yarn_queues():
    result = list_queues()
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/hadoop/queues/{queue_name}")
def get_yarn_queue(queue_name: str):
    result = get_queue_info(queue_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/hadoop/scheduler")
def get_scheduler_raw():
    result = get_raw_scheduler_info()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
