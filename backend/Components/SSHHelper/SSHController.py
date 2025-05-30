from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
import json
import httpx

from SSHHelper import (
    create_ssh_client,
    run_ssh_command,
    upload_file,
    download_file,
    close_ssh_client
)

router = APIRouter()
REDIS_API_URL = "" 

# Models
class SSHConnectionRequest(BaseModel):
    session_id: str
    hostname: str
    port: int = 22
    username: str
    password: Optional[str] = None
    key_path: Optional[str] = None

class SSHCommandRequest(BaseModel):
    session_id: str
    command: str

class SSHFileActionRequest(BaseModel):
    session_id: str
    remote_path: str
    local_path: Optional[str] = None

class SSHCloseRequest(BaseModel):
    session_id: str

async def redis_set_key(key: str, value: str, expire: int | None = None):
    async with httpx.AsyncClient() as client:
        payload = {"key": key, "value": value}
        if expire:
            payload["expire"] = expire
        await client.post(f"{REDIS_API_URL}/set", json=payload)

async def redis_get_key(key: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{REDIS_API_URL}/get", json={"key": key})
        if response.status_code == 404:
            return None
        return response.json()["value"]

async def redis_delete_key(key: str):
    async with httpx.AsyncClient() as client:
        await client.delete(f"{REDIS_API_URL}/delete", json={"key": key})

@router.post("/ssh/connect")
async def connect_ssh(req: SSHConnectionRequest):
    try:
        client = create_ssh_client(
            hostname=req.hostname,
            port=req.port,
            username=req.username,
            password=req.password,
            key_path=req.key_path
        )
        close_ssh_client(client)

        config_json = json.dumps(req.dict(exclude={"session_id"}))
        await redis_set_key(f"ssh:session:{req.session_id}", config_json)
        return {"status": "connection info stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ssh/run")
async def run_command(req: SSHCommandRequest):
    try:
        config_json = await redis_get_key(f"ssh:session:{req.session_id}")
        if not config_json:
            raise HTTPException(status_code=404, detail="Session not found")
        config = json.loads(config_json)

        client = create_ssh_client(**config)
        result = run_ssh_command(client, req.command)
        close_ssh_client(client)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ssh/upload")
async def upload_file_to_remote(session_id: str, remote_path: str, file: UploadFile = File(...)):
    try:
        config_json = await redis_get_key(f"ssh:session:{session_id}")
        if not config_json:
            raise HTTPException(status_code=404, detail="SSH session not found")
        config = json.loads(config_json)

        client = create_ssh_client(**config)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        result = upload_file(client, tmp_path, remote_path)
        os.remove(tmp_path)
        close_ssh_client(client)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ssh/download")
async def download_file_from_remote(req: SSHFileActionRequest):
    try:
        config_json = await redis_get_key(f"ssh:session:{req.session_id}")
        if not config_json:
            raise HTTPException(status_code=404, detail="SSH session not found")
        config = json.loads(config_json)

        client = create_ssh_client(**config)
        local_path = req.local_path or f"/tmp/{os.path.basename(req.remote_path)}"
        result = download_file(client, req.remote_path, local_path)
        close_ssh_client(client)
        return {"local_path": local_path, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ssh/close")
async def close_session(req: SSHCloseRequest):
    try:
        await redis_delete_key(f"ssh:session:{req.session_id}")
        return {"status": "session deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))