from fastapi import APIRouter, Header, HTTPException
from BoxTagManagerHelper import (
    create_tag,
    delete_tag,
    list_tags,
    attach_tag,
    detach_tag,
)

router = APIRouter(prefix="/box/tags", tags=["Box Tags"])

@router.post("/")
def api_create_tag(tag_name: str, authorization: str = Header(...)):
    try:
        return create_tag(authorization.replace("Bearer ", ""), tag_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{tag_id}")
def api_delete_tag(tag_id: str, authorization: str = Header(...)):
    try:
        return delete_tag(authorization.replace("Bearer ", ""), tag_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file/{file_id}")
def api_list_tags(file_id: str, authorization: str = Header(...)):
    try:
        return list_tags(authorization.replace("Bearer ", ""), file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file/{file_id}/attach")
def api_attach_tag(file_id: str, tag_name: str, authorization: str = Header(...)):
    try:
        return attach_tag(authorization.replace("Bearer ", ""), file_id, tag_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file/{file_id}/detach")
def api_detach_tag(file_id: str, tag_name: str, authorization: str = Header(...)):
    try:
        return detach_tag(authorization.replace("Bearer ", ""), file_id, tag_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))