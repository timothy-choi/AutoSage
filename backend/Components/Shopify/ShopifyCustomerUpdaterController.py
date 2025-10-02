from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from ShopifyCustomerUpdaterHelper import update_customer

router = APIRouter(prefix="/shopify/customers", tags=["Shopify Customer Updater"])

class UpdateCustomerRequest(BaseModel):
    shop_name: str
    customer_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    tags: Optional[str] = None
    addresses: Optional[List[Dict]] = None  


@router.put("/update")
def api_update_customer(request: UpdateCustomerRequest, access_token: str = Header(...)):
    try:
        return update_customer(
            shop_name=request.shop_name,
            access_token=access_token,
            customer_id=request.customer_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            tags=request.tags,
            addresses=request.addresses
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))