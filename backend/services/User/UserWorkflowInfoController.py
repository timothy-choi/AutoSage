from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from resources.database import SessionLocal, engine
from UserWorkflowInfoModel import UserWorkflowInfo
app = FastAPI()

class WorkflowInfo:
    user_id: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/UserWorkflowInfo/{user_workflow_info_id}")
def get_user_workflow_info(user_workflow_info_id: str, db: Session = Depends(get_db)):
    user_workflow_info = db.query(UserWorkflowInfo).filter(UserWorkflowInfo.id == user_workflow_info_id).first()

    if not user_workflow_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_workflow_info.to_dict(), 200

@app.get("/UserWorkflowInfo/user_id/{user_id}")
def get_user_workflow_info_by_user_id(user_id: str, db: Session = Depends(get_db)):
    user_workflow_info = db.query(UserWorkflowInfo).filter(UserWorkflowInfo.user_id == user_id).first()

    if not user_workflow_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_workflow_info.to_dict(), 200

@app.post("/UserWorklowInfo")
def create_user_workflow_info(workflow_info: WorkflowInfo, db: Session = Depends(get_db)):
    try:
        db.add(workflow_info)
        db.commit()
        db.refresh(workflow_info)
        return workflow_info.to_dict(), 201
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/UserWorkflowInfo/{user_workflow_info_id}")
def delete_user_workflow_info(user_workflow_info_id: str, db: Session = Depends(get_db)):
    try:
        workflow_info = db.query(UserWorkflowInfo).filter(UserWorkflowInfo.id == user_workflow_info_id).first()

        if workflow_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(workflow_info)
        db.commit()

        return None, 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
