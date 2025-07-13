from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from DropBoxToGoogleDriveMigratorHelper import migrate_dropbox_files_to_gdrive
from google.oauth2.credentials import Credentials

router = APIRouter()

class GoogleDriveCredentials(BaseModel):
    token: str
    refresh_token: Optional[str] = None
    token_uri: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    scopes: Optional[List[str]] = None

class DropboxToGDriveRequest(BaseModel):
    dropbox_access_token: str = Field(..., description="Dropbox API access token")
    dropbox_paths: List[str] = Field(..., description="List of Dropbox file paths to migrate")
    gdrive_credentials: GoogleDriveCredentials = Field(..., description="Google Drive OAuth2 credentials")
    gdrive_folder_id: Optional[str] = Field(None, description="Google Drive folder ID to upload files into")

@router.post("/dropbox/to/gdrive/migrate")
def dropbox_to_gdrive_migrate(request: DropboxToGDriveRequest):
    try:
        creds = Credentials(
            token=request.gdrive_credentials.token,
            refresh_token=request.gdrive_credentials.refresh_token,
            token_uri=request.gdrive_credentials.token_uri,
            client_id=request.gdrive_credentials.client_id,
            client_secret=request.gdrive_credentials.client_secret,
            scopes=request.gdrive_credentials.scopes
        )
        result = migrate_dropbox_files_to_gdrive(
            dropbox_token=request.dropbox_access_token,
            gdrive_creds=creds,
            dropbox_paths=request.dropbox_paths,
            gdrive_folder_id=request.gdrive_folder_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))