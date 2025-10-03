from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyCollectionListerHelper import (
    list_custom_collections,
    list_smart_collections,
    search_collections_by_title,
)

router = APIRouter(prefix="/shopify/collections", tags=["Shopify Collection Lister"])

class ListCollectionsRequest(BaseModel):
    shop_name: str
    limit: Optional[int] = 10
    page_info: Optional[str] = None

class SearchCollectionsRequest(BaseModel):
    shop_name: str
    title: str
    smart: Optional[bool] = False
    limit: Optional[int] = 10


@router.post("/list/custom")
def api_list_custom_collections(request: ListCollectionsRequest, access_token: str = Header(...)):
    try:
        return list_custom_collections(request.shop_name, access_token, request.limit, request.page_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/list/smart")
def api_list_smart_collections(request: ListCollectionsRequest, access_token: str = Header(...)):
    try:
        return list_smart_collections(request.shop_name, access_token, request.limit, request.page_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search")
def api_search_collections(request: SearchCollectionsRequest, access_token: str = Header(...)):
    try:
        return search_collections_by_title(
            request.shop_name, access_token, request.title, smart=request.smart, limit=request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))