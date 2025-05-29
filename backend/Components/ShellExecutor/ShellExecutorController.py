from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ShellExecutorHelper import (
    run_shell_command,
    run_shell_script,
    list_running_processes,
    kill_process_by_name,
    check_command_available
)

router = APIRouter()

# Request Models
class ShellCommand(BaseModel):
    command: str
    capture_output: bool = True
    timeout: int = 10

class ScriptExecutionRequest(BaseModel):
    script_path: str
    args: Optional[List[str]] = []

class KillProcessRequest(BaseModel):
    process_name: str

class CommandCheckRequest(BaseModel):
    command: str

# Endpoints

@router.post("/shell/run")
def run_shell(data: ShellCommand):
    result = run_shell_command(
        command=data.command,
        capture_output=data.capture_output,
        timeout=data.timeout
    )
    if result["exit_code"] == -1:
        raise HTTPException(status_code=500, detail=result["stderr"])
    return result

@router.post("/shell/script")
def execute_script(data: ScriptExecutionRequest):
    result = run_shell_script(data.script_path, data.args)
    if result["exit_code"] == -1:
        raise HTTPException(status_code=500, detail=result["stderr"])
    return result

@router.get("/shell/processes")
def list_processes():
    result = list_running_processes()
    if result["exit_code"] == -1:
        raise HTTPException(status_code=500, detail=result["stderr"])
    return result

@router.post("/shell/kill")
def kill_process(data: KillProcessRequest):
    result = kill_process_by_name(data.process_name)
    if result["exit_code"] == -1:
        raise HTTPException(status_code=500, detail=result["stderr"])
    return result

@router.post("/shell/check")
def check_command(data: CommandCheckRequest):
    result = check_command_available(data.command)
    if not result["available"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result