from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookToInstagramBridgeHelper import cross_post_facebook_to_instagram

router = APIRouter()

class FacebookPostInput(BaseModel):
    image_url: str
    caption: str

@router.post("/facebook/bridge/instagram")
def bridge_to_instagram(payload: FacebookPostInput):
    try:
        result = cross_post_facebook_to_instagram(payload.dict())
        return {"status": "posted", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))