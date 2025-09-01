from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any
import tempfile
import os
from AsanaAttachmentUploaderHelper import AsanaAttachmentUploaderHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaAttachmentUploaderHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaAttachmentUploaderHelper(token)
    return helper_instances[token]

@router.post("/asana/attachment/upload")
async def upload_attachment(token: str, task_gid: str, file: UploadFile = File(...)) -> Dict[str, Any]:
    helper = get_helper(token)

    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = helper.upload_attachment(task_gid, temp_path)

    os.remove(temp_path)

    return result

@router.get("/asana/attachment/list")
def list_attachments(token: str, task_gid: str) -> Dict[str, Any]:
    helper = get_helper(token)
    return helper.list_attachments(task_gid)