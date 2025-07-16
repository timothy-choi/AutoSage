from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from FigmaProjectCreatorHelper import (
    create_figma_team_project,
    list_team_projects,
    rename_project,
    delete_project,
    get_project_details
)

router = APIRouter()

class CreateProjectRequest(BaseModel):
    team_id: str = Field(..., description="Figma team ID where project will be created")
    project_name: str = Field(..., description="Name of the new Figma project")

class RenameProjectRequest(BaseModel):
    project_id: str = Field(..., description="Figma project ID")
    new_name: str = Field(..., description="New name for the project")

class DeleteProjectRequest(BaseModel):
    project_id: str = Field(..., description="Figma project ID")

class ProjectDetailsRequest(BaseModel):
    project_id: str = Field(..., description="Figma project ID")

@router.post("/figma/project/create")
async def create_project(req: CreateProjectRequest):
    try:
        return await create_figma_team_project(req.team_id, req.project_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/figma/projects")
async def list_projects(team_id: str = Query(..., description="Figma team ID")):
    try:
        return await list_team_projects(team_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/figma/project/rename")
async def rename_project_endpoint(req: RenameProjectRequest):
    try:
        return await rename_project(req.project_id, req.new_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/figma/project/delete")
async def delete_project_endpoint(req: DeleteProjectRequest):
    try:
        return await delete_project(req.project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/figma/project/details")
async def project_details(project_id: str = Query(..., description="Figma project ID")):
    try:
        return await get_project_details(project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
