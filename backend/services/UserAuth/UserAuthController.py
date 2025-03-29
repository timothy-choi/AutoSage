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