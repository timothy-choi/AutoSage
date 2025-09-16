from fastapi import APIRouter
from typing import List
from BoxFileCopyHelper import BoxFileCopierHelper

router = APIRouter()
helper_instances = {}

def get_helper(access_token: str) -> BoxFileCopierHelper:
    if access_token not in helper_instances:
        helper_instances[access_token] = BoxFileCopierHelper(access_token)
    return helper_instances[access_token]

@router.post("/box/file/{file_id}/copy")
def copy_file(access_token: str, file_id: str, new_parent_id: str):
    helper = get_helper(access_token)
    return helper.copy_file(file_id, new_parent_id)

@router.post("/box/file/{file_id}/copy-rename")
def copy_file_and_rename(access_token: str, file_id: str, new_parent_id: str, new_name: str):
    helper = get_helper(access_token)
    return helper.copy_file_and_rename(file_id, new_parent_id, new_name)

@router.post("/box/files/batch-copy")
def batch_copy_files(access_token: str, file_ids: List[str], new_parent_id: str):
    helper = get_helper(access_token)
    return helper.batch_copy_files(file_ids, new_parent_id)

@router.post("/box/folder/{folder_id}/copy-pattern")
def copy_files_by_pattern(access_token: str, folder_id: str, pattern: str, new_parent_id: str):
    helper = get_helper(access_token)
    return helper.copy_files_by_pattern(folder_id, pattern, new_parent_id)

@router.get("/box/folder/{folder_id}/preview-copy-pattern")
def preview_copy_by_pattern(access_token: str, folder_id: str, pattern: str):
    helper = get_helper(access_token)
    return {"files_to_copy": helper.preview_copy_by_pattern(folder_id, pattern)}