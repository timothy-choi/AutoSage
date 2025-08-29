from fastapi import APIRouter
from typing import Optional
from AsanaTaskEditorHelper import AsanaTaskEditorHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTaskEditorHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTaskEditorHelper(token)
    return helper_instances[token]

@router.put("/asana/task/update")
def update_task(
    token: str,
    task_gid: str,
    name: Optional[str] = None,
    notes: Optional[str] = None,
    assignee: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
):
    helper = get_helper(token)
    return helper.update_task(task_gid, name, notes, assignee, due_date, completed)

@router.post("/asana/task/add-project")
def add_project(token: str, task_gid: str, project_gid: str):
    helper = get_helper(token)
    return helper.add_project(task_gid, project_gid)

@router.post("/asana/task/remove-project")
def remove_project(token: str, task_gid: str, project_gid: str):
    helper = get_helper(token)
    return helper.remove_project(task_gid, project_gid)

@router.post("/asana/task/add-tag")
def add_tag(token: str, task_gid: str, tag_gid: str):
    helper = get_helper(token)
    return helper.add_tag(task_gid, tag_gid)

@router.post("/asana/task/remove-tag")
def remove_tag(token: str, task_gid: str, tag_gid: str):
    helper = get_helper(token)
    return helper.remove_tag(task_gid, tag_gid)