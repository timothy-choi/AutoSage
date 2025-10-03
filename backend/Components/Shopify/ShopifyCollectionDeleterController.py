from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List
from ShopifyCollectionDeleterHelper import (
    delete_custom_collection,
    delete_smart_collection,
    bulk_delete_custom_collections,
    bulk_delete_smart_collections,
)

router = APIRouter(prefix="/shopify/collections", tags=["Shopify Collection Deleter"])

class DeleteCollectionRequest(BaseModel):
    shop_name: str
    collection_id: str

class BulkDeleteRequest(BaseModel):
    shop_name: str
    collection_ids: List[str]


@router.delete("/custom")
def api_delete_custom_collection(request: DeleteCollectionRequest, access_token: str = Header(...)):
    try:
        return delete_custom_collection(request.shop_name, access_token, request.collection_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/smart")
def api_delete_smart_collection(request: DeleteCollectionRequest, access_token: str = Header(...)):
    try:
        return delete_smart_collection(request.shop_name, access_token, request.collection_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/bulk/custom")
def api_bulk_delete_custom(request: BulkDeleteRequest, access_token: str = Header(...)):
    try:
        return bulk_delete_custom_collections(request.shop_name, access_token, request.collection_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/bulk/smart")
def api_bulk_delete_smart(request: BulkDeleteRequest, access_token: str = Header(...)):
    try:
        return bulk_delete_smart_collections(request.shop_name, access_token, request.collection_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))