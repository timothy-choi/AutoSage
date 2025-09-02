from fastapi import APIRouter
from typing import Dict
from AsanaProjectDeleterHelper import AsanaProjectDeleterHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaProjectDeleterHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaProjectDeleterHelper(token)
    return helper_instances[token]

@router.delete("/asana/project/delete")
def delete_project(token: str, project_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.delete_project(project_gid)

@router.put("/asana/project/archive")
def archive_project(token: str, project_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.archive_project(project_gid)