from fastapi import APIRouter
from typing import Dict, Any
from AsanaProjectCreatorHelper import AsanaProjectCreatorHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaProjectCreatorHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaProjectCreatorHelper(token)
    return helper_instances[token]

@router.post("/asana/project/create")
def create_project(token: str, workspace_gid: str, name: str, team_gid: str = None, notes: str = None) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.create_project(workspace_gid, name, team_gid, notes)

@router.get("/asana/project/list")
def list_projects(token: str, workspace_gid: str, team_gid: str = None) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.list_projects(workspace_gid, team_gid)