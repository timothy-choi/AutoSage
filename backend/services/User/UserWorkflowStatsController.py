from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from resources.database import SessionLocal, engine
from UserWorkflowStats import UserWorkflowStats
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/UserWorkflowStats/{user_workflow_stats_id}")
def get_user_workflow_stats(user_workflow_stats_id: str, db: Session = Depends(get_db)):
    user_workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

    if not user_workflow_stats:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_workflow_stats.to_dict(), 200

@app.get("/UserWorkflowStats/user_id/{user_id}")
def get_user_workflow_stats_by_user_id(user_id: str, db: Session = Depends(get_db)):
    user_workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.user_id == user_id).first()

    if not user_workflow_stats:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_workflow_stats.to_dict(), 200

@app.post("/UserWorkflowStats")
def create_user_workflow_stats(workflow_stats: UserWorkflowStats, db: Session = Depends(get_db)):
    try:
        db.add(workflow_stats)
        db.commit()
        db.refresh(workflow_stats)
        return workflow_stats.to_dict(), 201
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/UserWorkflowStats/{user_workflow_stats_id}")
def delete_user_workflow_stats(user_workflow_stats_id: str, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(workflow_stats)
        db.commit()

        return None, 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))