from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from ShopifyProductImageManagerHelper import add_image, update_image, delete_image, list_images

router = APIRouter(prefix="/shopify/images", tags=["Shopify Product Image Manager"])

class AddImageRequest(BaseModel):
    shop_name: str
    product_id: str
    image_src: Optional[str] = None
    alt: Optional[str] = None
    position: Optional[int] = None


class UpdateImageRequest(BaseModel):
    shop_name: str
    product_id: str
    image_id: str
    alt: Optional[str] = None
    position: Optional[int] = None


class DeleteImageRequest(BaseModel):
    shop_name: str
    product_id: str
    image_id: str


@router.post("/add")
def api_add_image(request: AddImageRequest, access_token: str = Header(...)):
    try:
        return add_image(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            image_src=request.image_src,
            alt=request.alt,
            position=request.position
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update")
def api_update_image(request: UpdateImageRequest, access_token: str = Header(...)):
    try:
        return update_image(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            image_id=request.image_id,
            alt=request.alt,
            position=request.position
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
def api_delete_image(request: DeleteImageRequest, access_token: str = Header(...)):
    try:
        return delete_image(
            shop_name=request.shop_name,
            access_token=access_token,
            product_id=request.product_id,
            image_id=request.image_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list/{shop_name}/{product_id}")
def api_list_images(shop_name: str, product_id: str, access_token: str = Header(...)):
    try:
        return list_images(shop_name=shop_name, access_token=access_token, product_id=product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))