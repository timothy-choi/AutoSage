from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from SecretsManagerHelper import store_secret, retrieve_secret, delete_secret

router = APIRouter()

class SecretData(BaseModel):
    name: str
    value: str
    description: Optional[str] = ""

class SecretName(BaseModel):
    name: str
    force_delete: Optional[bool] = False

@router.post("/secrets/store")
async def store_secret_endpoint(data: SecretData):
    try:
        store_secret(name=data.name, secret_value=data.value, description=data.description)
        return {"status": "secret stored or updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/secrets/get")
async def retrieve_secret_endpoint(data: SecretName):
    try:
        value = retrieve_secret(data.name)
        return {"name": data.name, "value": value}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/secrets/delete")
async def delete_secret_endpoint(data: SecretName):
    try:
        delete_secret(data.name, force_delete=data.force_delete)
        return {"status": "secret deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))