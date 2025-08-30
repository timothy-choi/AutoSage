from fastapi import APIRouter
from typing import List
from AsanaTaskCompleterHelper import AsanaTaskCompleterHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTaskCompleterHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTaskCompleterHelper(token)
    return helper_instances[token]

@router.put("/asana/task/complete")
def complete_task(token: str, task_gid: str):
    helper = get_helper(token)
    return helper.complete_task(task_gid)

@router.put("/asana/task/uncomplete")
def uncomplete_task(token: str, task_gid: str):
    helper = get_helper(token)
    return helper.uncomplete_task(task_gid)

@router.put("/asana/task/bulk-complete")
def bulk_complete_tasks(token: str, task_gids: List[str]):
    helper = get_helper(token)
    return helper.bulk_complete_tasks(task_gids)

@router.put("/asana/task/bulk-uncomplete")
def bulk_uncomplete_tasks(token: str, task_gids: List[str]):
    helper = get_helper(token)
    return helper.bulk_uncomplete_tasks(task_gids)