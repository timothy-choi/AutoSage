from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from GoogleDriveFileUploaderHelper import upload_file_to_drive

router = APIRouter()

@router.post("/gdrive/upload")
async def upload_to_drive(
    access_token: str = Form(..., description="OAuth 2.0 access token"),
    file: UploadFile = File(...),
    file_name: str = Form(...),
    mime_type: str = Form(...),
    parent_folder_id: str = Form(None)
):
    try:
        file_bytes = await file.read()
        return upload_file_to_drive(
            access_token=access_token,
            file_content=file_bytes,
            file_name=file_name,
            mime_type=mime_type,
            parent_folder_id=parent_folder_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))