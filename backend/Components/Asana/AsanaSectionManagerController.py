from fastapi import APIRouter
from typing import Dict
from AsanaSectionManagerHelper import AsanaSectionManagerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaSectionManagerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaSectionManagerHelper(token)
    return helper_instances[token]

@router.post("/asana/section/create")
def create_section(token: str, project_gid: str, name: str) -> Dict:
    helper = get_helper(token)
    return helper.create_section(project_gid, name)

@router.put("/asana/section/update")
def update_section(token: str, section_gid: str, name: str) -> Dict:
    helper = get_helper(token)
    return helper.update_section(section_gid, name)

@router.delete("/asana/section/delete")
def delete_section(token: str, section_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.delete_section(section_gid)

@router.get("/asana/sections/list")
def list_sections(token: str, project_gid: str) -> Dict:
    helper = get_helper(token)
    return helper.list_sections(project_gid)