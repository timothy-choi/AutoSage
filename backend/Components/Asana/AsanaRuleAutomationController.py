from fastapi import APIRouter
from typing import Dict, List
from AsanaRuleAutomationHelper import AsanaRuleAutomationHelper

router = APIRouter()
helper_instances = {}


def get_helper(token: str) -> AsanaRuleAutomationHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaRuleAutomationHelper(token)
    return helper_instances[token]


@router.post("/asana/workspace/{workspace_gid}/rules/run")
def run_rule(token: str, workspace_gid: str, filters: Dict, actions: List[Dict]):
    helper = get_helper(token)
    return helper.run_rule(workspace_gid, filters, actions)