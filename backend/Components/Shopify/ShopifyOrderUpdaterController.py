from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from ShopifyOrderUpdaterHelper import (
    update_order,
    update_order_tags,
    update_order_note,
    update_order_email,
    close_order,
    reopen_order,
)

router = APIRouter(prefix="/shopify/orders", tags=["Shopify Order Updater"])

class OrderUpdateRequest(BaseModel):
    shop_name: str
    order_id: str
    updates: Dict[str, Optional[str]]

class OrderFieldUpdateRequest(BaseModel):
    shop_name: str
    order_id: str
    value: str


@router.put("/update")
def api_update_order(request: OrderUpdateRequest, access_token: str = Header(...)):
    try:
        return update_order(request.shop_name, access_token, request.order_id, request.updates)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update/tags")
def api_update_order_tags(request: OrderFieldUpdateRequest, access_token: str = Header(...)):
    try:
        return update_order_tags(request.shop_name, access_token, request.order_id, request.value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update/note")
def api_update_order_note(request: OrderFieldUpdateRequest, access_token: str = Header(...)):
    try:
        return update_order_note(request.shop_name, access_token, request.order_id, request.value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update/email")
def api_update_order_email(request: OrderFieldUpdateRequest, access_token: str = Header(...)):
    try:
        return update_order_email(request.shop_name, access_token, request.order_id, request.value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/close")
def api_close_order(request: OrderFieldUpdateRequest, access_token: str = Header(...)):
    try:
        return close_order(request.shop_name, access_token, request.order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reopen")
def api_reopen_order(request: OrderFieldUpdateRequest, access_token: str = Header(...)):
    try:
        return reopen_order(request.shop_name, access_token, request.order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))