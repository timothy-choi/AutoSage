from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchOBSHelper import start_streaming, stop_streaming, switch_scene

router = APIRouter()

class SceneSwitchRequest(BaseModel):
    scene_name: str

@router.post("/twitch/obs/start-stream")
async def obs_start_stream():
    result = await start_streaming()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/twitch/obs/stop-stream")
async def obs_stop_stream():
    result = await stop_streaming()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/twitch/obs/switch-scene")
async def obs_switch_scene(req: SceneSwitchRequest):
    result = await switch_scene(req.scene_name)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    return result