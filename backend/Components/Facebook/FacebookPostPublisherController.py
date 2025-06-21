from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookPostPublisherHelper import (
    publish_facebook_post,
    publish_photo_post
)

router = APIRouter()

class FacebookPostPayload(BaseModel):
    message: str

class FacebookPhotoPostPayload(BaseModel):
    image_url: str
    caption: str

@router.post("/facebook/post")
def create_facebook_post(payload: FacebookPostPayload):
    try:
        post_id = publish_facebook_post(payload.message)
        return {"status": "posted", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/post/photo")
def create_facebook_photo_post(payload: FacebookPhotoPostPayload):
    try:
        post_id = publish_photo_post(payload.image_url, payload.caption)
        return {"status": "photo_posted", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))