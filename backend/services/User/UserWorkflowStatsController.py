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
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/total_workflows_created/{total_workflows_created}")
def update_total_workflows_created(user_workflow_stats_id: str, total_workflows_created: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.total_workflows_created = total_workflows_created
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/total_workflow_executions/{total_workflow_executions}")
def update_total_workflow_executions(user_workflow_stats_id: str, total_workflow_executions: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.total_workflow_executions = total_workflow_executions
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/successful_executions/{successful_executions}")
def update_successful_executions(user_workflow_stats_id: str, successful_executions: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.successful_executions = successful_executions
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/failed_executions/{failed_executions}")
def update_failed_executions(user_workflow_stats_id: str, failed_executions: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.failed_executions = failed_executions
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/api_calls_made/{api_calls_made}")
def update_api_calls_made(user_workflow_stats_id: str, api_calls_made: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.api_calls_made = api_calls_made
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/active_workflows/{active_workflows}")
def update_active_workflows(user_workflow_stats_id: str, active_workflows: int, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.active_workflows = active_workflows
        db.commit()

        return workflow_stats.to_dict(), 200
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/UserWorkflowStats/{user_workflow_stats_id}/most_used_workflow/{most_used_workflow}")
def update_most_used_workflow(user_workflow_stats_id: str, most_used_workflow: str, db: Session = Depends(get_db)):
    try:
        workflow_stats = db.query(UserWorkflowStats).filter(UserWorkflowStats.id == user_workflow_stats_id).first()

        if workflow_stats is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        workflow_stats.most_used_workflow = most_used_workflow
        db.commit()

        return workflow_stats.to_dict(), 200
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