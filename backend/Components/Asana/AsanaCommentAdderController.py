from fastapi import APIRouter
from typing import Dict, Any
from AsanaCommentAdderHelper import AsanaCommentAdderHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaCommentAdderHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaCommentAdderHelper(token)
    return helper_instances[token]

@router.post("/asana/comment/add")
def add_comment(token: str, task_gid: str, text: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.add_comment(task_gid, text)

@router.get("/asana/comment/list")
def list_comments(token: str, task_gid: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.list_comments(task_gid)