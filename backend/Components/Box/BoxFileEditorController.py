from fastapi import APIRouter, UploadFile
from BoxFileEditorHelper import BoxFileEditorHelper
import tempfile
import shutil

router = APIRouter()
helper_instances = {}


def get_helper(access_token: str) -> BoxFileEditorHelper:
    if access_token not in helper_instances:
        helper_instances[access_token] = BoxFileEditorHelper(access_token)
    return helper_instances[access_token]


@router.put("/box/file/{file_id}/rename")
def rename_file(access_token: str, file_id: str, new_name: str):
    helper = get_helper(access_token)
    return helper.rename_file(file_id, new_name)


@router.put("/box/file/{file_id}/upload-version")
def upload_new_version(access_token: str, file_id: str, file: UploadFile):
    helper = get_helper(access_token)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return helper.upload_new_version(file_id, temp_file.name)


@router.put("/box/file/{file_id}/replace-text")
def replace_text_in_file(access_token: str, file_id: str, replacements: dict):
    helper = get_helper(access_token)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    return helper.replace_text_in_file(file_id, replacements, temp_file.name)