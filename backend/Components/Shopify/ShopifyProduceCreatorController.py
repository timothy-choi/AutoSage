from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ShopifyProductCreatorHelper import create_product

router = APIRouter(prefix="/shopify/products", tags=["Shopify Product Creator"])

class ProductCreateRequest(BaseModel):
    shop_name: str
    title: str
    body_html: Optional[str] = ""
    vendor: Optional[str] = ""
    product_type: Optional[str] = ""
    tags: Optional[List[str]] = None
    price: Optional[float] = None


@router.post("/create")
def api_create_product(request: ProductCreateRequest, access_token: str = Header(...)):
    try:
        return create_product(
            shop_name=request.shop_name,
            access_token=access_token,
            title=request.title,
            body_html=request.body_html,
            vendor=request.vendor,
            product_type=request.product_type,
            tags=request.tags,
            price=request.price
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))