from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TwitchRewardResponderHelper import respond_to_channel_point_reward

router = APIRouter()

class RewardRequest(BaseModel):
    oauth_token: str
    client_id: str
    reward_id: str
    user_input: str
    message: str

@router.post("/twitch/respond-to-reward")
async def respond_to_reward(req: RewardRequest):
    result = await respond_to_channel_point_reward(
        req.oauth_token,
        req.client_id,
        req.reward_id,
        req.user_input,
        req.message
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
