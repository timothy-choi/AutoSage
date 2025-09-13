from fastapi import APIRouter, UploadFile
from BoxFileUploaderHelper import BoxFileUploaderHelper
import tempfile
import shutil

router = APIRouter()
helper_instances = {}


def get_helper(access_token: str) -> BoxFileUploaderHelper:
    if access_token not in helper_instances:
        helper_instances[access_token] = BoxFileUploaderHelper(access_token)
    return helper_instances[access_token]


@router.post("/box/upload/{folder_id}")
def upload_file(access_token: str, folder_id: str, file: UploadFile):
    helper = get_helper(access_token)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = helper.upload_file(folder_id, temp_file.name)

    return result