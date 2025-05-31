from fastapi import APIRouter, HTTPException, Query
from HadoopFileInspectorHelper import (
    create_hdfs_client,
    list_hdfs_directory,
    get_file_info,
    list_all_files_recursive
)

router = APIRouter()

client = create_hdfs_client()

@router.get("/hdfs/list")
def list_directory(path: str = "/"):
    result = list_hdfs_directory(client, path)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/hdfs/info")
def file_info(path: str):
    result = get_file_info(client, path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/hdfs/list-recursive")
def list_recursive(path: str = "/"):
    result = list_all_files_recursive(client, path)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result