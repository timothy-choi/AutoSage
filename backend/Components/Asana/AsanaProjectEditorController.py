from fastapi import APIRouter
from typing import Dict, Any
from AsanaProjectEditorHelper import AsanaProjectEditorHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaProjectEditorHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaProjectEditorHelper(token)
    return helper_instances[token]

@router.put("/asana/project/update")
def update_project(token: str, project_gid: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.update_project(project_gid, fields)

@router.get("/asana/project/get")
def get_project(token: str, project_gid: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.get_project(project_gid)
