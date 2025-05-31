from fastapi import APIRouter, HTTPException, Query
from HadoopHealthCheckerHelper import (
    check_namenode_health,
    check_yarn_health,
    check_hdfs_summary
)

router = APIRouter()

@router.get("/health/namenode")
def namenode_health(host: str = Query("localhost"), port: int = Query(9870)):
    result = check_namenode_health(host, port)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/health/yarn")
def yarn_health(host: str = Query("localhost"), port: int = Query(8088)):
    result = check_yarn_health(host, port)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/health/hdfs")
def hdfs_summary(host: str = Query("localhost"), port: int = Query(9870)):
    result = check_hdfs_summary(host, port)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
