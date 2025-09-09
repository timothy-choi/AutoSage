from fastapi import APIRouter
from typing import Dict
from AsanaUserManagerHelper import AsanaUserManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaUserManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaUserManagerHelper(token)
    return helper_instances[token]

@router.get("/asana/workspace/{workspace_gid}/users")
def list_users(token: str, workspace_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_users(workspace_gid)

@router.get("/asana/user/{user_gid}")
def get_user(token: str, user_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.get_user(user_gid)

@router.get("/asana/user/me")
def get_current_user(token: str) -> Dict:
    helper = get_helper(token)
    return helper.get_current_user()