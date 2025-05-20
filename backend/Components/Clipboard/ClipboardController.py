from fastapi import FastAPI, Form, Query
from fastapi.responses import JSONResponse
from ClipboardHelper import *

app = FastAPI()

@app.post("/clipboard/copy")
def api_copy_to_clipboard(text: str = Form(...)):
    try:
        copy_to_clipboard(text)
        return {"status": "copied"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/clipboard/paste")
def api_paste_from_clipboard():
    try:
        text = paste_from_clipboard()
        return {"clipboard": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/clipboard/clear")
def api_clear_clipboard():
    try:
        clear_clipboard()
        return {"status": "clipboard cleared"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/clipboard/is-empty")
def api_is_clipboard_empty():
    try:
        empty = is_clipboard_empty()
        return {"is_empty": empty}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/clipboard/history")
def api_get_clipboard_history(limit: int = Query(10)):
    try:
        return {"history": get_clipboard_history(limit)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/clipboard/changed")
def api_has_clipboard_changed(last_value: str = Query(...)):
    try:
        changed = has_clipboard_changed(last_value)
        return {"changed": changed}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/clipboard/wait")
def api_wait_for_clipboard_change(last_value: str = Query(...), timeout: float = Query(10.0)):
    try:
        new_value = wait_for_clipboard_change(last_value, timeout)
        return {"new_value": new_value}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})