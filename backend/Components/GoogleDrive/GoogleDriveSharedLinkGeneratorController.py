from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveSharedLinkGeneratorHelper import generate_shared_link

router = APIRouter()

class SharedLinkRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 token with Drive access")
    file_id: str = Field(..., description="ID of the file or folder to share")
    role: str = Field("reader", description="Permission level: reader or writer")

@router.post("/gdrive/generate-shared-link")
def generate_link(request: SharedLinkRequest):
    try:
        return generate_shared_link(
            access_token=request.access_token,
            file_id=request.file_id,
            role=request.role
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))