from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyOrderFetcherHelper import (
    fetch_orders,
    fetch_order_by_id,
    fetch_orders_by_customer,
    fetch_orders_by_date_range,
)

router = APIRouter(prefix="/shopify/orders", tags=["Shopify Order Fetcher"])

class FetchOrdersRequest(BaseModel):
    shop_name: str
    status: Optional[str] = "any"
    limit: Optional[int] = 10
    page_info: Optional[str] = None

class FetchOrderByIdRequest(BaseModel):
    shop_name: str
    order_id: str

class FetchOrdersByCustomerRequest(BaseModel):
    shop_name: str
    customer_id: str
    limit: Optional[int] = 10

class FetchOrdersByDateRangeRequest(BaseModel):
    shop_name: str
    created_at_min: str
    created_at_max: str
    limit: Optional[int] = 10


@router.post("/list")
def api_fetch_orders(request: FetchOrdersRequest, access_token: str = Header(...)):
    try:
        return fetch_orders(request.shop_name, access_token, request.status, request.limit, request.page_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get")
def api_fetch_order_by_id(request: FetchOrderByIdRequest, access_token: str = Header(...)):
    try:
        return fetch_order_by_id(request.shop_name, access_token, request.order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/customer")
def api_fetch_orders_by_customer(request: FetchOrdersByCustomerRequest, access_token: str = Header(...)):
    try:
        return fetch_orders_by_customer(request.shop_name, access_token, request.customer_id, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/date-range")
def api_fetch_orders_by_date_range(request: FetchOrdersByDateRangeRequest, access_token: str = Header(...)):
    try:
        return fetch_orders_by_date_range(
            request.shop_name, access_token, request.created_at_min, request.created_at_max, request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))