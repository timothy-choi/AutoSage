from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ShopifyProductUpdaterHelper import update_product

router = APIRouter(prefix="/shopify/products", tags=["Shopify Product Updater"])

class ProductUpdateRequest(BaseModel):
    shop_name: str
    product_id: str
    title: Optional[str] = None
    body_html: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    tags: Optional[List[str]] = None
    price: Optional[float] = None


@router.put("/update")
def api_update_product(request: ProductUpdateRequest, access_token: str = Header(...)):
    try:
        return update_product(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            title=request.title,
            body_html=request.body_html,
            vendor=request.vendor,
            product_type=request.product_type,
            tags=request.tags,
            price=request.price
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))