from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List
from NotificationManagerModel import NotificationManager
from backend.resources import get_db 

app = FastAPI()

@app.post("/notification-manager/", response_model=NotificationManager, status_code=201)
def create_notification_manager(data: NotificationManager, db: Session = Depends(get_db)):
    nm = NotificationManager(**data.dict(), id=uuid4(), all_user_notifications=[])
    db.add(nm)
    db.commit()
    db.refresh(nm)
    return nm

@app.get("/notification-manager/{notification_manager_id}", response_model=NotificationManager)
def get_by_id(notification_manager_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account not found")
    return nm

@app.get("/notification-manager/user/{user_id}", response_model=NotificationManager)
def get_by_user_id(user_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).filter_by(user_id=user_id).first()
    if not nm:
        raise HTTPException(status_code=404, detail="Account not found")
    return nm

@app.put("/notification-manager/notificationType/{notification_manager_id}/{notification_type}", response_model=NotificationManager)
def change_notification_type(notification_manager_id: UUID, notification_type: str, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    nm.notification_type = notification_type
    db.commit()
    db.refresh(nm)
    return nm

@app.put("/notification-manager/showNotification/{notification_manager_id}", response_model=NotificationManager)
def toggle_show_notification(notification_manager_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    nm.show_notifications = not nm.show_notifications
    db.commit()
    db.refresh(nm)
    return nm

@app.put("/notification-manager/allUserNotifications/{notification_manager_id}/{notification_id}", response_model=NotificationManager)
def add_notification(notification_manager_id: UUID, notification_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    if notification_id not in nm.all_user_notifications:
        nm.all_user_notifications.append(notification_id)
    db.commit()
    db.refresh(nm)
    return nm

@app.put("/notification-manager/allUserNotifications/remove/{notification_manager_id}/{notification_id}", response_model=NotificationManager)
def remove_notification(notification_manager_id: UUID, notification_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    if notification_id in nm.all_user_notifications:
        nm.all_user_notifications.remove(notification_id)
    db.commit()
    db.refresh(nm)
    return nm

@app.put("/notification-manager/notificationToken/{notification_manager_id}", response_model=NotificationManager)
def set_notification_token(notification_manager_id: UUID, token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    nm.user_token = token
    db.commit()
    db.refresh(nm)
    return nm

@app.delete("/notification-manager/{notification_manager_id}", status_code=200)
def delete_notification_manager(notification_manager_id: UUID, db: Session = Depends(get_db)):
    nm = db.query(NotificationManager).get(notification_manager_id)
    if not nm:
        raise HTTPException(status_code=404, detail="Account does not exist")
    db.delete(nm)
    db.commit()
    return {"message": "successfully deleted"}