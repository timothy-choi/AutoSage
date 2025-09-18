from fastapi import APIRouter, Depends
from pydantic import BaseModel
from BoxCollaboratorManagerHelper import (
    add_collaborator,
    remove_collaborator,
    list_collaborators,
    update_collaborator_role
)

router = APIRouter(prefix="/box/collaborators", tags=["Box Collaborators"])

class CollaboratorAddRequest(BaseModel):
    folder_id: str
    email: str
    role: str = "editor"

class CollaboratorUpdateRequest(BaseModel):
    collaboration_id: str
    new_role: str

class CollaboratorRemoveRequest(BaseModel):
    collaboration_id: str

@router.post("/add")
def add_box_collaborator(data: CollaboratorAddRequest, client):
    return add_collaborator(client, data.folder_id, data.email, data.role)

@router.post("/remove")
def remove_box_collaborator(data: CollaboratorRemoveRequest, client):
    return remove_collaborator(client, data.collaboration_id)

@router.get("/list/{folder_id}")
def list_box_collaborators(folder_id: str, client):
    return list_collaborators(client, folder_id)

@router.post("/update-role")
def update_box_collaborator_role(data: CollaboratorUpdateRequest, client):
    return update_collaborator_role(client, data.collaboration_id, data.new_role)