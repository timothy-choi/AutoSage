from fastapi import APIRouter
from typing import Dict, Any
from AsanaSubtaskManagerHelper import AsanaSubtaskManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaSubtaskManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaSubtaskManagerHelper(token)
    return helper_instances[token]

@router.post("/asana/subtask/create")
def create_subtask(token: str, parent_task_gid: str, name: str, notes: str = "") -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.create_subtask(parent_task_gid, name, notes)

@router.get("/asana/subtask/list")
def list_subtasks(token: str, parent_task_gid: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.list_subtasks(parent_task_gid)

@router.put("/asana/subtask/update")
def update_subtask(token: str, subtask_gid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.update_subtask(subtask_gid, updates)

@router.delete("/asana/subtask/delete")
def delete_subtask(token: str, subtask_gid: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.delete_subtask(subtask_gid)