from fastapi import APIRouter, UploadFile, File, Form
from ConfluenceAttachmentUploaderHelper import upload_attachment_to_confluence

router = APIRouter()

@router.post("/confluence/upload-attachment")
async def upload_confluence_attachment(
    page_id: str = Form(...),
    file: UploadFile = File(...)
):
    result = await upload_attachment_to_confluence(page_id, file)
    return result