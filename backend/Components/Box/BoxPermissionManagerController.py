from fastapi import APIRouter, Header, Query
from typing import Dict, Any
from BoxPermissionManagerHelper import BoxPermissionManagerHelper

router = APIRouter()
API_BASE = "https://api.box.com/2.0"

def get_helper(authorization: str) -> BoxPermissionManagerHelper:
    """Utility to create helper with runtime token."""
    headers = {"Authorization": authorization}
    return BoxPermissionManagerHelper(API_BASE, headers)

@router.post("/box/{item_type}/{item_id}/collaborators")
def add_collaborator(
    item_id: str,
    item_type: str,
    user_login: str = Query(..., description="Email/login of user to add"),
    role: str = Query(..., description="Role to assign (editor, viewer, etc.)"),
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.add_collaborator(item_id, item_type, user_login, role)

@router.delete("/box/collaborations/{collaboration_id}")
def remove_collaborator(
    collaboration_id: str,
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.remove_collaborator(collaboration_id)

@router.put("/box/collaborations/{collaboration_id}/role")
def update_collaborator_role(
    collaboration_id: str,
    new_role: str = Query(..., description="New role for collaborator"),
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.update_collaborator_role(collaboration_id, new_role)

@router.get("/box/{item_type}/{item_id}/collaborators")
def list_collaborators(
    item_id: str,
    item_type: str,
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.list_collaborators(item_id, item_type)

@router.put("/box/{item_type}/{item_id}/shared-link")
def set_shared_link(
    item_id: str,
    item_type: str,
    access: str = Query("open", description="Access level (open, company, collaborators)"),
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.set_shared_link(item_id, item_type, access)

@router.delete("/box/{item_type}/{item_id}/shared-link")
def revoke_shared_link(
    item_id: str,
    item_type: str,
    authorization: str = Header(...),
) -> Dict[str, Any]:
    helper = get_helper(authorization)
    return helper.revoke_shared_link(item_id, item_type)