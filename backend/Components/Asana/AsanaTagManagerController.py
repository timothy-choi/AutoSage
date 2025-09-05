from fastapi import APIRouter
from typing import Dict, Optional
from AsanaTagManagerHelper import AsanaTagManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTagManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTagManagerHelper(token)
    return helper_instances[token]

@router.post("/asana/tag/create")
def create_tag(token: str, workspace_gid: str, name: str, color: Optional[str] = None) -> Dict:
    helper = get_helper(token)
    return helper.create_tag(workspace_gid, name, color)

@router.get("/asana/tag/{tag_gid}")
def get_tag(token: str, tag_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.get_tag(tag_gid)

@router.put("/asana/tag/{tag_gid}")
def update_tag(token: str, tag_gid: str, name: Optional[str] = None, color: Optional[str] = None) -> Dict:
    helper = get_helper(token)
    return helper.update_tag(tag_gid, name, color)

@router.delete("/asana/tag/{tag_gid}")
def delete_tag(token: str, tag_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.delete_tag(tag_gid)

@router.post("/asana/task/{task_gid}/add_tag/{tag_gid}")
def add_tag_to_task(token: str, task_gid: str, tag_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.add_tag_to_task(task_gid, tag_gid)

@router.post("/asana/task/{task_gid}/remove_tag/{tag_gid}")
def remove_tag_from_task(token: str, task_gid: str, tag_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.remove_tag_from_task(task_gid, tag_gid)

@router.get("/asana/workspace/{workspace_gid}/tags")
def list_tags_in_workspace(token: str, workspace_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_tags_in_workspace(workspace_gid)