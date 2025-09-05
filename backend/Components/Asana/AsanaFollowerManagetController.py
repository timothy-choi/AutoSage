from fastapi import APIRouter
from typing import Dict
from AsanaFollowerManagerHelper import AsanaFollowerManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaFollowerManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaFollowerManagerHelper(token)
    return helper_instances[token]

@router.post("/asana/task/{task_gid}/add_follower/{user_gid}")
def add_follower(token: str, task_gid: str, user_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.add_follower(task_gid, user_gid)

@router.post("/asana/task/{task_gid}/remove_follower/{user_gid}")
def remove_follower(token: str, task_gid: str, user_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.remove_follower(task_gid, user_gid)

@router.get("/asana/task/{task_gid}/followers")
def list_followers(token: str, task_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_followers(task_gid)