from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Optional, Any
from WebhookNotifierHelper import *

app = FastAPI()

class WebhookRequest(BaseModel):
    webhook_url: str
    payload: Optional[Dict[str, Any]] = {}
    headers: Optional[Dict[str, str]] = None
    timeout: Optional[int] = 5

class TextWebhookRequest(BaseModel):
    webhook_url: str
    message: str
    headers: Optional[Dict[str, str]] = None
    timeout: Optional[int] = 5

class FormWebhookRequest(BaseModel):
    webhook_url: str
    form_data: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None
    timeout: Optional[int] = 5

class AuthWebhookRequest(BaseModel):
    webhook_url: str
    payload: Optional[Dict[str, Any]] = {}
    token: str
    timeout: Optional[int] = 5

@app.post("/webhook/json")
def webhook_json(data: WebhookRequest):
    try:
        result = send_webhook(data.webhook_url, data.payload, data.headers, data.timeout)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/webhook/text")
def webhook_text(data: TextWebhookRequest):
    try:
        result = send_text_webhook(data.webhook_url, data.message, data.headers, data.timeout)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/webhook/form")
def webhook_form(data: FormWebhookRequest):
    try:
        result = send_form_webhook(data.webhook_url, data.form_data, data.headers, data.timeout)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/webhook/auth")
def webhook_auth(data: AuthWebhookRequest):
    try:
        result = send_webhook_with_auth(data.webhook_url, data.payload, data.token, data.timeout)
        return result
    except Exception as e:
        return {"error": str(e)}
