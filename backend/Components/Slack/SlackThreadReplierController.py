from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from SlackThreadReplierHelper import reply_to_slack_thread, upload_slack_file

router = APIRouter()

class ThreadReplyRequest(BaseModel):
    token: str
    channel: str
    thread_ts: str
    message: str

@router.post("/slack/reply-thread")
def reply_to_thread(data: ThreadReplyRequest):
    try:
        result = reply_to_slack_thread(data.token, data.channel, data.thread_ts, data.message)

        if not result.get("ok"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {
            "message": "Reply sent successfully",
            "thread_ts": data.thread_ts,
            "response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from fastapi import UploadFile, Form
@router.post("/slack/reply-attachment")
async def reply_with_file_attachment(
    token: str = Form(...),
    channel: str = Form(...),
    thread_ts: str = Form(...),
    file: UploadFile = Form(...)
):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    result = upload_slack_file(token, channel, file_path, title=f"Reply to thread {thread_ts}")
    return {"uploaded_file": result}