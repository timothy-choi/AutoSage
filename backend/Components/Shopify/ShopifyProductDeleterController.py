from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from typing import List
from ShopifyProductDeleterHelper import (
    delete_product,
    bulk_delete_products,
    delete_products_by_tag,
    delete_products_older_than,
    soft_delete_product
)

router = APIRouter(prefix="/shopify/products", tags=["Shopify Product Deleter"])

class DeleteProductRequest(BaseModel):
    shop_name: str
    product_id: str

class BulkDeleteRequest(BaseModel):
    shop_name: str
    product_ids: List[str]

class DeleteByTagRequest(BaseModel):
    shop_name: str
    tag: str

class DeleteOlderRequest(BaseModel):
    shop_name: str
    days: int


@router.delete("/delete")
def api_delete_product(request: DeleteProductRequest, access_token: str = Header(...)):
    try:
        return delete_product(request.shop_name, access_token, request.product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/bulk-delete")
def api_bulk_delete_products(request: BulkDeleteRequest, access_token: str = Header(...)):
    try:
        return bulk_delete_products(request.shop_name, access_token, request.product_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete-by-tag")
def api_delete_by_tag(request: DeleteByTagRequest, access_token: str = Header(...)):
    try:
        return delete_products_by_tag(request.shop_name, access_token, request.tag)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete-older")
def api_delete_older(request: DeleteOlderRequest, access_token: str = Header(...)):
    try:
        return delete_products_older_than(request.shop_name, access_token, request.days)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/soft-delete")
def api_soft_delete(request: DeleteProductRequest, access_token: str = Header(...)):
    try:
        return soft_delete_product(request.shop_name, access_token, request.product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))