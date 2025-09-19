from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from BoxSharedLinkGeneratorHelper import create_shared_link, revoke_shared_link

router = APIRouter(prefix="/box/shared-link", tags=["Box Shared Link"])

# Request models
class SharedLinkCreateRequest(BaseModel):
    item_id: str
    item_type: str = "file"  
    access: str = "open"   
    can_download: bool = True
    can_preview: bool = True

class SharedLinkRevokeRequest(BaseModel):
    item_id: str
    item_type: str = "file"

@router.post("/create")
def create_box_shared_link(data: SharedLinkCreateRequest):
    permissions = {"can_download": data.can_download, "can_preview": data.can_preview}
    return create_shared_link(data.item_id, data.item_type, data.access, permissions)

@router.post("/revoke")
def revoke_box_shared_link(data: SharedLinkRevokeRequest):
    return revoke_shared_link(data.item_id, data.item_type)