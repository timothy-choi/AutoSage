from fastapi import APIRouter, Header
from typing import Dict, Any
from BoxFileVersionManagerHelper import BoxFileVersionManagerHelper

router = APIRouter()

API_BASE = "https://api.box.com/2.0"

def get_helper(authorization: str) -> BoxFileVersionManagerHelper:
    headers = {"Authorization": authorization}
    return BoxFileVersionManagerHelper(API_BASE, headers)

@router.get("/box/files/{file_id}/versions")
def list_file_versions(
    file_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.list_versions(file_id)

@router.post("/box/files/{file_id}/versions/{version_id}/promote")
def promote_file_version(
    file_id: str,
    version_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.promote_version(file_id, version_id)

@router.delete("/box/files/{file_id}/versions/{version_id}")
def delete_file_version(
    file_id: str,
    version_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.delete_version(file_id, version_id)