from fastapi import APIRouter, Header, Query
from typing import Dict, Any
from BoxFolderEditorController import BoxFolderEditorHelper

router = APIRouter()
API_BASE = "https://api.box.com/2.0"

def get_helper(authorization: str) -> BoxFolderEditorHelper:
    headers = {"Authorization": authorization}
    return BoxFolderEditorHelper(API_BASE, headers)

@router.put("/box/folders/{folder_id}/rename")
def rename_folder(
    folder_id: str,
    new_name: str = Query(..., description="New folder name"),
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.rename_folder(folder_id, new_name)

@router.put("/box/folders/{folder_id}/move")
def move_folder(
    folder_id: str,
    new_parent_id: str = Query(..., description="ID of the new parent folder"),
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.move_folder(folder_id, new_parent_id)

@router.put("/box/folders/{folder_id}/description")
def update_description(
    folder_id: str,
    description: str = Query(..., description="New folder description"),
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.update_description(folder_id, description)

@router.post("/box/folders/{folder_id}/lock")
def lock_folder(
    folder_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.lock_folder(folder_id)

@router.delete("/box/folders/{folder_id}/lock")
def unlock_folder(
    folder_id: str,
    authorization: str = Header(..., description="Bearer access token"),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.unlock_folder(folder_id)