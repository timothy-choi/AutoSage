from fastapi import APIRouter
from typing import Dict
from AsanaTaskManagerHelper import AsanaTaskManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTaskManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTaskManagerHelper(token)
    return helper_instances[token]

@router.post("/asana/task")
def create_task(token: str, workspace_gid: str, name: str, assignee: str = None, notes: str = None, projects: list = None) -> Dict:
    helper = get_helper(token)
    return helper.create_task(workspace_gid, name, assignee, notes, projects)

@router.get("/asana/task/{task_gid}")
def get_task(token: str, task_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.get_task(task_gid)

@router.put("/asana/task/{task_gid}")
def update_task(token: str, task_gid: str, updates: Dict) -> Dict:
    helper = get_helper(token)
    return helper.update_task(task_gid, updates)

@router.delete("/asana/task/{task_gid}")
def delete_task(token: str, task_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.delete_task(task_gid)

@router.post("/asana/task/{task_gid}/complete")
def complete_task(token: str, task_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.complete_task(task_gid)

@router.post("/asana/task/{task_gid}/assign/{user_gid}")
def assign_task(token: str, task_gid: str, user_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.assign_task(task_gid, user_gid)

@router.post("/asana/task/{task_gid}/move/{section_gid}")
def move_task_to_section(token: str, task_gid: str, section_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.move_task_to_section(task_gid, section_gid)