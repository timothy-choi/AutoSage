from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyProductVariantManagerHelper import add_variant, update_variant, delete_variant

router = APIRouter(prefix="/shopify/variants", tags=["Shopify Product Variant Manager"])

class AddVariantRequest(BaseModel):
    shop_name: str
    product_id: str
    option1: str
    price: float
    sku: Optional[str] = None
    inventory_quantity: Optional[int] = 0


class UpdateVariantRequest(BaseModel):
    shop_name: str
    variant_id: str
    option1: Optional[str] = None
    price: Optional[float] = None
    sku: Optional[str] = None
    inventory_quantity: Optional[int] = None


class DeleteVariantRequest(BaseModel):
    shop_name: str
    product_id: str
    variant_id: str


@router.post("/add")
def api_add_variant(request: AddVariantRequest, access_token: str = Header(...)):
    try:
        return add_variant(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            option1=request.option1,
            price=request.price,
            sku=request.sku,
            inventory_quantity=request.inventory_quantity
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update")
def api_update_variant(request: UpdateVariantRequest, access_token: str = Header(...)):
    try:
        return update_variant(
            shop_name=request.shop_name,
            access_token=access_token,
            variant_id=request.variant_id,
            option1=request.option1,
            price=request.price,
            sku=request.sku,
            inventory_quantity=request.inventory_quantity
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
def api_delete_variant(request: DeleteVariantRequest, access_token: str = Header(...)):
    try:
        return delete_variant(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            variant_id=request.variant_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))