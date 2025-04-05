from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from Notification import Notification 
from backend.resources import get_db  

app = FastAPI()


@app.get("/notification/{notification_id}", response_model=Notification)
def get_notification_by_id(notification_id: UUID, db: Session = Depends(get_db)):
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@app.post("/notification/", response_model=Notification, status_code=status.HTTP_201_CREATED)
def create_notification(notification_data: Notification, db: Session = Depends(get_db)):
    notification = Notification(
        id=uuid4(),
        **notification_data.dict()
    )
    db.add(notification)
    try:
        db.commit()
        db.refresh(notification)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return notification


@app.delete("/notification/{notification_id}", status_code=200)
def delete_notification(notification_id: UUID, db: Session = Depends(get_db)):
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    try:
        db.delete(notification)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"msg": "successful"}
