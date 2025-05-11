from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile
import shutil
import os
import OpenAIHelper

app = FastAPI()


def validate_required_fields(data: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")


class ChatRequest(BaseModel):
    messages: list
    model: str = "gpt-4"


class TextCompletionRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo-instruct"


class AssistantCreateRequest(BaseModel):
    name: str
    instructions: str
    model: str = "gpt-4"
    file_ids: list = []
    tools: list = []


class AddMessageRequest(BaseModel):
    thread_id: str
    content: str
    file_ids: list = []


class RunAssistantRequest(BaseModel):
    thread_id: str
    assistant_id: str
    instructions: str = None


class WaitForRunCompletionRequest(BaseModel):
    thread_id: str
    run_id: str
    poll_interval: float = 1.0


class ThreadRequest(BaseModel):
    thread_id: str


class DeleteRequest(BaseModel):
    assistant_id: str


@app.post("/OpenAI/Chat")
async def generate_chat_completion(req: ChatRequest):
    try:
        validate_required_fields(req.dict(), ["messages"])
        response = OpenAIHelper.generate_chat_completion(req.messages, req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/TextCompletion")
async def generate_text_completion(req: TextCompletionRequest):
    try:
        validate_required_fields(req.dict(), ["prompt"])
        response = OpenAIHelper.generate_text_completion(req.prompt, req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/UploadFile")
async def upload_file(file: UploadFile = File(...), purpose: str = Form("assistants")):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No selected file")
        
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = OpenAIHelper.upload_file(file_path, purpose)

        os.remove(file_path)
        os.rmdir(temp_dir)

        return {"file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/CreateAssistant")
async def create_assistant(req: AssistantCreateRequest):
    try:
        validate_required_fields(req.dict(), ["name", "instructions"])
        assistant_id = OpenAIHelper.create_assistant(**req.dict())
        return {"assistant_id": assistant_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/CreateThread")
async def create_thread():
    try:
        thread_id = OpenAIHelper.create_thread()
        return {"thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/AddMessageToThread")
async def add_message_to_thread(req: AddMessageRequest):
    try:
        validate_required_fields(req.dict(), ["thread_id", "content"])
        message_id = OpenAIHelper.add_message_to_thread(
            thread_id=req.thread_id, content=req.content, file_ids=req.file_ids
        )
        return {"message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/RunAssistant")
async def run_assistant(req: RunAssistantRequest):
    try:
        validate_required_fields(req.dict(), ["thread_id", "assistant_id"])
        run_id = OpenAIHelper.run_assistant(
            thread_id=req.thread_id,
            assistant_id=req.assistant_id,
            instructions=req.instructions
        )
        return {"run_id": run_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/WaitForRunCompletion")
async def wait_for_run_completion(req: WaitForRunCompletionRequest):
    try:
        validate_required_fields(req.dict(), ["thread_id", "run_id"])
        status = OpenAIHelper.wait_for_run_completion(
            thread_id=req.thread_id,
            run_id=req.run_id,
            poll_interval=req.poll_interval
        )
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/OpenAI/GetThreadMessages")
async def get_thread_messages(req: ThreadRequest):
    try:
        validate_required_fields(req.dict(), ["thread_id"])
        messages = OpenAIHelper.get_thread_messages(req.thread_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/OpenAI/DeleteAssistant")
async def delete_assistant(req: DeleteRequest):
    try:
        validate_required_fields(req.dict(), ["assistant_id"])
        success = OpenAIHelper.delete_assistant(req.assistant_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/OpenAI/DeleteThread")
async def delete_thread(req: ThreadRequest):
    try:
        validate_required_fields(req.dict(), ["thread_id"])
        success = OpenAIHelper.delete_thread(req.thread_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
