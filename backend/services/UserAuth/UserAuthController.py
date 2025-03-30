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
    return user_auth.to_dict()

@app.get("/user_auth/user_id/{user_id}")
def get_user_auth_by_user_id(user_id: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.user_id == user_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict()

@app.get("/user_auth/username/{username}")
def get_user_auth_by_username(username: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.username == username).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict()

@app.get("/user_auth/email/{email}")
def get_user_auth_by_email(email: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.email == email).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    return user_auth.to_dict()

@app.post("/user_auth/")
def create_user_auth(user_auth: UserAuth, db: Session = Depends(get_db)):
    db.add(user_auth)
    db.commit()
    db.refresh(user_auth)
    return user_auth.to_dict()

@app.put("/user_auth/{user_auth_id}/username/{original_username}/{updated_username}")  
def update_username(user_auth_id: str, original_username: str, updated_username: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    if user_auth.username != original_username:
        raise HTTPException(status_code=400, detail="Original username does not match")
    user_auth.username = updated_username
    db.commit()
    db.refresh(user_auth)
    return user_auth.to_dict()

@app.put("/user_auth/{user_auth_id}/email/{original_email}/{updated_email}")
def update_email(user_auth_id: str, original_email: str, updated_email: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    if user_auth.email != original_email:
        raise HTTPException(status_code=400, detail="Original email does not match")
    user_auth.email = updated_email
    db.commit()
    db.refresh(user_auth)
    return user_auth.to_dict()

@app.delete("/user_auth/{user_auth_id}")
def delete_user_auth(user_auth_id: str, db: Session = Depends(get_db)):
    user_auth = db.query(UserAuth).filter(UserAuth.id == user_auth_id).first()
    if user_auth is None:
        raise HTTPException(status_code=404, detail="UserAuth not found")
    db.delete(user_auth)
    db.commit()
    return user_auth.to_dict()