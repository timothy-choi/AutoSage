from fastapi import APIRouter, Query
from typing import List, Optional
from AsanaTaskCreatorHelper import AsanaTaskCreatorHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str, workspace_gid: str, project_gid: Optional[str] = None) -> AsanaTaskCreatorHelper:
    key = f"{workspace_gid}:{project_gid}:{token}"
    if key not in helper_instances:
        helper_instances[key] = AsanaTaskCreatorHelper(token, workspace_gid, project_gid)
    return helper_instances[key]

@router.post("/asana/task/create")
def create_task(
    token: str,
    workspace_gid: str,
    name: str,
    notes: str = "",
    project_gid: Optional[str] = None,
    assignee: Optional[str] = None,
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = Query(default=None),
):
    helper = get_helper(token, workspace_gid, project_gid)
    return helper.create_task(name, notes, assignee, due_date, tags)

@router.get("/asana/projects")
def list_projects(token: str, workspace_gid: str):
    helper = get_helper(token, workspace_gid)
    return helper.list_projects()

@router.get("/asana/users")
def list_users(token: str, workspace_gid: str):
    helper = get_helper(token, workspace_gid)
    return helper.list_users()