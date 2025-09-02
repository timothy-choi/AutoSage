from fastapi import APIRouter
from typing import Dict
from AsanaWorkspaceManagerHelper import AsanaWorkspaceManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaWorkspaceManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaWorkspaceManagerHelper(token)
    return helper_instances[token]

@router.get("/asana/workspaces/list")
def list_workspaces(token: str) -> Dict:
    helper = get_helper(token)
    return helper.list_workspaces()

@router.get("/asana/workspace/get")
def get_workspace(token: str, workspace_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.get_workspace(workspace_gid)

@router.put("/asana/workspace/update")
def update_workspace(token: str, workspace_gid: str, name: str) -> Dict:
    helper = get_helper(token)
    return helper.update_workspace(workspace_gid, name)

@router.get("/asana/workspace/users")
def list_users_in_workspace(token: str, workspace_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_users_in_workspace(workspace_gid)