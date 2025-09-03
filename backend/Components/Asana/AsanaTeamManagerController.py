from fastapi import APIRouter
from typing import Dict
from AsanaTeamManagerHelper import AsanaTeamManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaTeamManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaTeamManagerHelper(token)
    return helper_instances[token]

@router.get("/asana/workspace/{workspace_gid}/teams")
def list_teams_in_workspace(token: str, workspace_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_teams_in_workspace(workspace_gid)

@router.get("/asana/team/{team_gid}")
def get_team(token: str, team_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.get_team(team_gid)

@router.get("/asana/team/{team_gid}/users")
def list_users_in_team(token: str, team_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_users_in_team(team_gid)

@router.post("/asana/team/{team_gid}/add_user")
def add_user_to_team(token: str, team_gid: str, user_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.add_user_to_team(team_gid, user_gid)

@router.delete("/asana/team/membership/{membership_gid}")
def remove_user_from_team(token: str, membership_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.remove_user_from_team(membership_gid)