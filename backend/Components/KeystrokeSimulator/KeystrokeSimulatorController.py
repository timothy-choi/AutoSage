from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from KeystrokeSimulatorHelper import *

app = FastAPI()

class TextInput(BaseModel):
    text: str
    interval: Optional[float] = 0.05

class KeyInput(BaseModel):
    key: str

class HotkeyInput(BaseModel):
    keys: List[str]

class HoldKeyInput(BaseModel):
    key: str
    duration: float

class KeySequenceInput(BaseModel):
    keys: List[str]
    interval: Optional[float] = 0.1

class RepeatKeyInput(BaseModel):
    key: str
    count: int
    interval: Optional[float] = 0.05

class DelayTypingInput(BaseModel):
    text: str
    start_delay: float
    interval: Optional[float] = 0.05

@app.post("/keystroke/type")
def api_type_text(data: TextInput):
    try:
        type_text(data.text, data.interval)
        return {"status": "typed"}
    except Exception as e:
        return {'error': str(e)}

@app.post("/keystroke/press")
def api_press_key(data: KeyInput):
    try:
        press_key(data.key)
        return {"status": "key pressed"}
    except Exception as e:
        return {'error': str(e)}

@app.post("/keystroke/hotkey")
def api_hotkey(data: HotkeyInput):
    try:
        hotkey_combination(*data.keys)
        return {"status": "hotkey pressed"}
    except Exception as e:
        return {'error': str(e)}
    
@app.post("/keystroke/hold")
def api_hold_key(data: HoldKeyInput):
    try:
        hold_key(data.key, data.duration)
        return {"status": "key held"}
    except Exception as e:
        return {'error': str(e)}
    
@app.post("/keystroke/sequence")
def api_press_sequence(data: KeySequenceInput):
    try:
        press_keys_sequence(data.keys, data.interval)
        return {"status": "sequence complete"}
    except Exception as e:
        return {'error': str(e)}
    
@app.post("/keystroke/clear")
def api_clear_line():
    try:
        clear_line()
        return {"status": "line cleared"}
    except Exception as e:
        return {'error': str(e)}
    
@app.post("/keystroke/repeat")
def api_repeat_key(data: RepeatKeyInput):
    try:
        repeat_key(data.key, data.count, data.interval)
        return {"status": "key repeated"}
    except Exception as e:
        return {'error': str(e)}
    
@app.post("/keystroke/delay")
def api_delay_typing(data: DelayTypingInput):
    try:
        delay_typing(data.text, data.start_delay, data.interval)
        return {"status": "delayed typing complete"}
    except Exception as e:
        return {'error': str(e)}