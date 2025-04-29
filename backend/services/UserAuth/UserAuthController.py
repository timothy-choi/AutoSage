from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from resources.database import SessionLocal, engine
from UserAuth import UserAuth  

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user_auth/{user_auth_id}")
def get_user_auth(user_auth_id: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict(), 200

@app.get("/user_auth/user_id/{user_id}")
def get_user_auth_by_user_id(user_id: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.user_id == user_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict(), 200

@app.get("/user_auth/username/{username}")
def get_user_auth_by_username(username: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.username == username).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict(), 200

@app.get("/user_auth/email/{email}")
def get_user_auth_by_email(email: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.email == email).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict(), 200

@app.post("/user_auth/")
def create_user_auth(user_auth: UserAuth, db: Session = Depends(get_db)):
    try:
        db.add(user_auth)
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 201
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/user_auth/user_id/{user_auth_id}/{user_id}}")
def update_user_id(user_auth_id: str, user_id: str, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        user_auth.user_id = user_id
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user_auth/{user_auth_id}/username/{original_username}/{updated_username}")  
def update_username(user_auth_id: str, original_username: str, updated_username: str, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        if user_auth.username != original_username:
            raise HTTPException(status_code=400, detail="Original username does not match")
        user_auth.username = updated_username
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put('/user_auth/password/{user_auth_id}')
def change_user_password(user_auth_id: str, pass_info: dict, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()

        if not user_auth:
            raise HTTPException(status_code=404, detail="UserAuth not found")

        user_auth.password = pass_info['password']

        user_auth.hash_value = pass_info['hash_value']

        db.commit()

        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user_auth/{user_auth_id}/email/{original_email}/{updated_email}")
def update_email(user_auth_id: str, original_email: str, updated_email: str, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        if user_auth.email != original_email:
            raise HTTPException(status_code=400, detail="Original email does not match")
        user_auth.email = updated_email
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user_auth/{user_auth_id}/google_oauth")
def update_google_oauth(user_auth_id: str, google_oauth: dict, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        user_auth.google_oauth = google_oauth
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user_auth/{user_auth_id}/is_verified/{is_verified}")
def update_is_verified(user_auth_id: str, is_verified: bool, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        user_auth.is_verified = is_verified
        db.commit()
        db.refresh(user_auth)
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/user_auth/{user_auth_id}")
def delete_user_auth(user_auth_id: str, db: Session = Depends(get_db)):
    try:
        user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
        if user_auth is None:
            raise HTTPException(status_code=404, detail="UserAuth not found")
        db.delete(user_auth)
        db.commit()
        return user_auth.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))