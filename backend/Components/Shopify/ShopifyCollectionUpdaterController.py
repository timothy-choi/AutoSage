from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyCollectionUpdaterHelper import update_custom_collection

router = APIRouter(prefix="/shopify/collections", tags=["Shopify Collection Updater"])

class UpdateCollectionRequest(BaseModel):
    shop_name: str
    collection_id: str
    title: Optional[str] = None
    body_html: Optional[str] = None
    image_src: Optional[str] = None
    sort_order: Optional[str] = None
    published: Optional[bool] = None


@router.put("/update")
def api_update_collection(request: UpdateCollectionRequest, access_token: str = Header(...)):
    try:
        return update_custom_collection(
            shop_name=request.shop_name,
            access_token=access_token,
            collection_id=request.collection_id,
            title=request.title,
            body_html=request.body_html,
            image_src=request.image_src,
            sort_order=request.sort_order,
            published=request.published
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))