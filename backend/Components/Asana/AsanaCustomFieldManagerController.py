from fastapi import APIRouter
from typing import Dict, List, Optional
from AsanaCustomFieldManagerHelper import AsanaCustomFieldManagerHelper

router = APIRouter()
helper_instances = {}


def get_helper(token: str) -> AsanaCustomFieldManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaCustomFieldManagerHelper(token)
    return helper_instances[token]


@router.get("/asana/workspace/{workspace_gid}/custom-fields")
def list_custom_fields(token: str, workspace_gid: str) -> List[Dict]:
    helper = get_helper(token)
    return helper.list_custom_fields(workspace_gid)


@router.post("/asana/workspace/{workspace_gid}/custom-fields")
def create_custom_field(
    token: str,
    workspace_gid: str,
    name: str,
    field_type: str,
    enum_options: Optional[List[str]] = None
) -> Dict:
    helper = get_helper(token)
    return helper.create_custom_field(workspace_gid, name, field_type, enum_options)


@router.put("/asana/custom-field/{field_gid}")
def update_custom_field(token: str, field_gid: str, updates: Dict) -> Dict:
    helper = get_helper(token)
    return helper.update_custom_field(field_gid, updates)


@router.delete("/asana/custom-field/{field_gid}")
def delete_custom_field(token: str, field_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.delete_custom_field(field_gid)


@router.post("/asana/project/{project_gid}/custom-field/{field_gid}/add")
def add_custom_field_to_project(token: str, project_gid: str, field_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.add_custom_field_to_project(project_gid, field_gid)


@router.post("/asana/project/{project_gid}/custom-field/{field_gid}/remove")
def remove_custom_field_from_project(token: str, project_gid: str, field_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.remove_custom_field_from_project(project_gid, field_gid)