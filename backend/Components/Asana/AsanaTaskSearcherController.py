from fastapi import APIRouter
from typing import Dict, Optional
from AsanaTaskSearcherHelper import AsanaTaskSearcherHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTaskSearcherHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTaskSearcherHelper(token)
    return helper_instances[token]

@router.get("/asana/project/{project_gid}/tasks/search")
def search_tasks_in_project(token: str, project_gid: str, text: Optional[str] = None, completed: Optional[bool] = None) -> Dict:
    helper = get_helper(token)
    params = {}
    if text:
        params["text"] = text
    if completed is not None:
        params["completed"] = str(completed).lower()
    return helper.search_tasks_in_project(project_gid, params)

@router.get("/asana/workspace/{workspace_gid}/tasks/search")
def search_tasks_in_workspace(token: str, workspace_gid: str, text: Optional[str] = None, completed: Optional[bool] = None) -> Dict:
    helper = get_helper(token)
    params = {}
    if text:
        params["text"] = text
    if completed is not None:
        params["completed"] = str(completed).lower()
    return helper.search_tasks_in_workspace(workspace_gid, params)

@router.get("/asana/workspace/{workspace_gid}/assignee/{assignee_gid}/tasks/search")
def search_tasks_by_assignee(token: str, workspace_gid: str, assignee_gid: str, completed: Optional[bool] = None) -> Dict:
    helper = get_helper(token)
    params = {}
    if completed is not None:
        params["completed"] = str(completed).lower()
    return helper.search_tasks_by_assignee(workspace_gid, assignee_gid, params)