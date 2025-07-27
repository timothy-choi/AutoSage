from fastapi import APIRouter, Body
from pydantic import BaseModel
from ConfluenceSpaceCreatorHelper import create_confluence_space

router = APIRouter()

class SpaceCreateRequest(BaseModel):
    key: str
    name: str
    description: str = ""

@router.post("/confluence/create-space")
async def create_space(req: SpaceCreateRequest):
    try:
        result = await create_confluence_space(
            key=req.key,
            name=req.name,
            description=req.description
        )
        return {"status": "success", "space": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}