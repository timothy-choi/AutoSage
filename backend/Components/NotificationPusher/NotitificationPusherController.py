from fastapi import FastAPI
from pydantic import BaseModel
from NotificationPusherHelper import *
app = FastAPI()

class NotificationInput(BaseModel):
    title: str
    message: str
    timeout: int = 5

class MessageInput(BaseModel):
    message: str

@app.post("/notify/push")
def api_push_notification(data: NotificationInput):
    try:
        push_notification(data.title, data.message, data.timeout)
        return {"status": "notification sent"}
    except Exception as e:
        return {"error": str(e)}