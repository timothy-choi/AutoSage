from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyCollectionCreatorHelper import create_custom_collection

router = APIRouter(prefix="/shopify/collections", tags=["Shopify Collection Creator"])

class CreateCollectionRequest(BaseModel):
    shop_name: str
    title: str
    body_html: Optional[str] = None
    image_src: Optional[str] = None
    sort_order: Optional[str] = "best-selling"
    published: Optional[bool] = True


@router.post("/create")
def api_create_collection(request: CreateCollectionRequest, access_token: str = Header(...)):
    try:
        return create_custom_collection(
            shop_name=request.shop_name,
            access_token=access_token,
            title=request.title,
            body_html=request.body_html,
            image_src=request.image_src,
            sort_order=request.sort_order,
            published=request.published
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))