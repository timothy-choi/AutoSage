from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from CommandInterpreterHelper import interpret_command, explain_command, suggest_command_variants

router = APIRouter()

class CommandInput(BaseModel):
    instruction: str

@router.post("/command/interpret")
def interpret(data: CommandInput):
    try:
        command = interpret_command(data.instruction)
        return {"shell_command": command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/command/explain")
def explain(data: CommandInput):
    try:
        explanation = explain_command(data.instruction)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/command/alternatives")
def alternatives(data: CommandInput):
    try:
        alternatives = suggest_command_variants(data.instruction)
        return {"alternatives": alternatives}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))