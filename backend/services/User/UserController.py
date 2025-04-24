from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from resources.database import SessionLocal, engine
from User import User 

app = FastAPI()

class LoginDate:
    login_date: datetime
    login_ip: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.to_dict() for user in users], 200

@app.get("/user/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict(), 200

@app.get("/user/username/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict(), 200

@app.post("/user/")
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.to_dict(), 201
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user/{user_id}/username/{original_username}/{updated_username}")
def update_username(user_id: str, original_username: str, updated_username: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.username != original_username:
            raise HTTPException(status_code=400, detail="Original username does not match")
        user.username = updated_username
        db.commit()
        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/email/{original_email}/{updated_email}")
def update_email(user_id: str, original_email: str, updated_email: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.email != original_email:
            raise HTTPException(status_code=400, detail="Original email does not match")
        user.email = updated_email
        db.commit()
        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/is_active")
def set_is_actve(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_active = True if not user.is_active else False

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/last_login_info")
def set_last_login_info(user_id: str, login_date: LoginDate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.last_login = login_date.login_date

        user.last_login_ip = login_date.login_ip

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/user/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
