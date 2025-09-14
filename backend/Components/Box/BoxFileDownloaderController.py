from fastapi import APIRouter, Response
from BoxFileDownloaderHelper import BoxFileDownloaderHelper

router = APIRouter()
helper_instances = {}


def get_helper(access_token: str) -> BoxFileDownloaderHelper:
    if access_token not in helper_instances:
        helper_instances[access_token] = BoxFileDownloaderHelper(access_token)
    return helper_instances[access_token]


@router.get("/box/download/{file_id}")
def download_file(access_token: str, file_id: str):
    helper = get_helper(access_token)
    result = helper.download_file(file_id)

    if "content" in result:
        return Response(content=result["content"], media_type="application/octet-stream",
                        headers={"Content-Disposition": f"attachment; filename={file_id}.bin"})
    else:
        return result