from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from WhatsAppTemplateManagerHelper import (
    create_template, update_template, get_template,
    delete_template, list_templates, send_template_message
)

router = APIRouter()

class TemplateCreatePayload(BaseModel):
    name: str
    content: str

class TemplateUpdatePayload(BaseModel):
    name: str
    content: str

class TemplateUsePayload(BaseModel):
    to: str
    name: str
    variables: Dict[str, str]

@router.post("/whatsapp/template/create")
def create(payload: TemplateCreatePayload):
    try:
        result = create_template(payload.name, payload.content)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/whatsapp/template/update")
def update(payload: TemplateUpdatePayload):
    try:
        result = update_template(payload.name, payload.content)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/whatsapp/template/get/{name}")
def get(name: str):
    try:
        content = get_template(name)
        return {"name": name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/whatsapp/template/delete/{name}")
def delete(name: str):
    try:
        result = delete_template(name)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/whatsapp/template/list")
def list_all():
    return list_templates()

@router.post("/whatsapp/template/send")
def send(payload: TemplateUsePayload):
    try:
        sid = send_template_message(payload.to, payload.name, payload.variables)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))