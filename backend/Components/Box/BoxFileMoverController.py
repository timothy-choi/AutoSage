from fastapi import APIRouter
from BoxFileMoverHelper import BoxFileMoverHelper

router = APIRouter()
helper_instances = {}


def get_helper(access_token: str) -> BoxFileMoverHelper:
    if access_token not in helper_instances:
        helper_instances[access_token] = BoxFileMoverHelper(access_token)
    return helper_instances[access_token]


@router.put("/box/file/{file_id}/move")
def move_file(access_token: str, file_id: str, new_parent_id: str):
    helper = get_helper(access_token)
    return helper.move_file(file_id, new_parent_id)
