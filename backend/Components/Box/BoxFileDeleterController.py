from fastapi import APIRouter, Query
from BoxFileDeleterHelper import delete_file

router = APIRouter()

@router.delete("/box/files/delete")
def delete_box_file(
    file_id: str = Query(..., description="ID of the Box file to delete"),
    access_token: str = Query(..., description="Box API access token")
):
    return delete_file(file_id, access_token)