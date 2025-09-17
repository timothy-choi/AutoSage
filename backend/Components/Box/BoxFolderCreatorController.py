from fastapi import APIRouter, Header, Query
from typing import Dict, Any
from BoxFolderCreatorHelper import BoxFolderCreatorHelper

router = APIRouter()
API_BASE = "https://api.box.com/2.0"

def get_helper(authorization: str) -> BoxFolderCreatorHelper:
    headers = {"Authorization": authorization}
    return BoxFolderCreatorHelper(API_BASE, headers)

@router.post("/box/folders")
def create_folder(
    name: str,
    parent_id: str = Query("0", description="Parent folder ID (default root: 0)"),
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.create_folder(name, parent_id)

@router.get("/box/folders/{folder_id}")
def get_folder_info(
    folder_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.get_folder_info(folder_id)

@router.get("/box/folders/{folder_id}/items")
def list_folder_items(
    folder_id: str,
    limit: int = Query(100, description="Max number of items to return"),
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.list_folder_items(folder_id, limit)