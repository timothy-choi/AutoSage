from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

class NotificationRequest(BaseModel):
    token: str
    title: str
    message: str
    link: Optional[str] = None

class GroupNotificationRequest(BaseModel):
    topic: str
    title: str
    message: str
    link: Optional[str] = None

class SubscribeRequest(BaseModel):
    device_token: str
    topic: str

@app.post("/userNotification")
def send_user_notification(data: NotificationRequest):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=data.title,
                body=data.message,
            ),
            token=data.token,
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title=data.title,
                    body=data.message
                ),
                fcm_options=messaging.WebpushFCMOptions(link=data.link),
            ),
        )
        response = messaging.send(message)
        return {"message": "Notification sent", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/groupNotification")
def send_group_notification(data: GroupNotificationRequest):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=data.title,
                body=data.message,
            ),
            topic=data.topic,
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title=data.title,
                    body=data.message
                ),
                fcm_options=messaging.WebpushFCMOptions(link=data.link),
            ),
        )
        response = messaging.send(message)
        return {"message": "Notification sent", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/subscribe")
def subscribe_to_topic(data: SubscribeRequest):
    try:
        messaging.subscribe_to_topic([data.device_token], data.topic)
        return {"message": f"Subscribed to topic: {data.topic}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))