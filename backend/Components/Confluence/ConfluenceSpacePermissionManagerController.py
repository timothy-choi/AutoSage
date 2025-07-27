from fastapi import APIRouter
from ConfluenceSpacePermissionManagerHelper import (
    set_space_permissions,
    list_space_permissions,
    remove_space_permission,
    check_user_permission,
)

router = APIRouter()

@router.post("/confluence/set-space-permissions")
async def set_permissions(space_key: str, permissions: list):
    try:
        result = await set_space_permissions(space_key, permissions)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/confluence/list-space-permissions/{space_key}")
async def get_space_permissions(space_key: str):
    try:
        result = await list_space_permissions(space_key)
        return {"status": "success", "permissions": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.delete("/confluence/remove-space-permission/{space_key}/{permission_id}")
async def delete_space_permission(space_key: str, permission_id: int):
    try:
        result = await remove_space_permission(space_key, permission_id)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/confluence/check-user-permission")
async def check_permission(space_key: str, user_account_id: str, permission_key: str):
    try:
        has_perm = await check_user_permission(space_key, user_account_id, permission_key)
        return {"status": "success", "has_permission": has_perm}
    except Exception as e:
        return {"status": "error", "message": str(e)}