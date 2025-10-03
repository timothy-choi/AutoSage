from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyProductListerHelper import (
    list_products,
    list_products_in_collection,
    list_products_by_vendor,
    search_products_by_title,
)

router = APIRouter(prefix="/shopify/products", tags=["Shopify Product Lister"])

class ListProductsRequest(BaseModel):
    shop_name: str
    limit: Optional[int] = 10
    page_info: Optional[str] = None

class ListCollectionRequest(BaseModel):
    shop_name: str
    collection_id: str
    limit: Optional[int] = 10

class ListVendorRequest(BaseModel):
    shop_name: str
    vendor: str
    limit: Optional[int] = 10

class SearchTitleRequest(BaseModel):
    shop_name: str
    title: str
    limit: Optional[int] = 10


@router.post("/list")
def api_list_products(request: ListProductsRequest, access_token: str = Header(...)):
    try:
        return list_products(request.shop_name, access_token, request.limit, request.page_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/list/collection")
def api_list_products_in_collection(request: ListCollectionRequest, access_token: str = Header(...)):
    try:
        return list_products_in_collection(request.shop_name, access_token, request.collection_id, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/list/vendor")
def api_list_products_by_vendor(request: ListVendorRequest, access_token: str = Header(...)):
    try:
        return list_products_by_vendor(request.shop_name, access_token, request.vendor, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search/title")
def api_search_products_by_title(request: SearchTitleRequest, access_token: str = Header(...)):
    try:
        return search_products_by_title(request.shop_name, access_token, request.title, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))