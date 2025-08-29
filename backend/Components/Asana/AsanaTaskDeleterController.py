from fastapi import APIRouter
from typing import List
from AsanaTaskDeleterHelper import AsanaTaskDeleterHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTaskDeleterHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTaskDeleterHelper(token)
    return helper_instances[token]

@router.delete("/asana/task/delete")
def delete_task(token: str, task_gid: str):
    helper = get_helper(token)
    return helper.delete_task(task_gid)

@router.delete("/asana/task/bulk-delete")
def bulk_delete_tasks(token: str, task_gids: List[str]):
    helper = get_helper(token)
    return helper.bulk_delete_tasks(task_gids)