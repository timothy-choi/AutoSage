from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from resources.database import SessionLocal, engine
from User import User, AccountPlans

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

@app.get("/user/email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
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
    
@app.put("/user/{user_id}/notification_manager")
def set_notification_manager(user_id: str, notification_manager_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.notification_manager_id = notification_manager_id

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/account_plan")
def set_account_plan(user_id: str, account_plan_val: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        if account_plan_val == 'free':
            user.account_plan = AccountPlans.FREE
        elif account_plan_val == 'pro':
            user.account_plan = AccountPlans.PRO
        else:
            user.account_plan = AccountPlans.ENTERPRISE

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/user_workflow_info_id")
def set_user_workflow_info_id(user_id: str, user_workflow_info_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.user_workflow_info_id = user_workflow_info_id

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/security_settings")
def set_security_settings(user_id: str, security_settings: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.security_settings = security_settings

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user/{user_id}/platform_settings")
def set_platform_settings(user_id: str, platform_settings: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.platform_settings = platform_settings

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/usage_settings")
def set_usage_settings(user_id: str, usage_settings: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.usage_settings = usage_settings

        db.commit()

        return user.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user/{user_id}/ui_preferences")
def set_ui_preferences(user_id: str, ui_preferences: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.ui_preferences = ui_preferences

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
