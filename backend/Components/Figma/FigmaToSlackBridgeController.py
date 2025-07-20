from fastapi import APIRouter
from pydantic import BaseModel
from FigmaToSlackBridgeHelper import (
    send_figma_update_to_slack,
    format_figma_comment_message,
    format_figma_activity_summary
)

router = APIRouter()

class FigmaToSlackCommentRequest(BaseModel):
    slack_webhook_url: str
    file_name: str
    commenter: str
    comment_text: str
    file_url: str

class FigmaToSlackActivityRequest(BaseModel):
    slack_webhook_url: str
    file_name: str
    last_modified: str
    file_url: str

@router.post("/figma/to-slack/comment")
def post_figma_comment_to_slack(req: FigmaToSlackCommentRequest):
    message = format_figma_comment_message(
        req.file_name, req.commenter, req.comment_text, req.file_url
    )
    return send_figma_update_to_slack(req.slack_webhook_url, message)

@router.post("/figma/to-slack/activity")
def post_figma_activity_to_slack(req: FigmaToSlackActivityRequest):
    message = format_figma_activity_summary(
        req.file_name, req.last_modified, req.file_url
    )
    return send_figma_update_to_slack(req.slack_webhook_url, message)