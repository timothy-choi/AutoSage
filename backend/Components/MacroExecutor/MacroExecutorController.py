from fastapi import FastAPI, Body, Form, Query
from fastapi.responses import JSONResponse
from MacroExecutorHelper import (
    execute_macro,
    validate_macro,
    summarize_macro,
    save_macro,
    load_macro,
    list_macros,
    run_saved_macro
)
from typing import List, Dict, Union

app = FastAPI()

MacroStep = Dict[str, Union[str, int, float, List[str]]]

@app.post("/macro/execute")
def api_execute_macro(steps: List[MacroStep] = Body(...)):
    try:
        if not validate_macro(steps):
            return JSONResponse(status_code=400, content={"error": "Invalid macro steps"})
        execute_macro(steps)
        return {"status": "executed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/macro/save")
def api_save_macro(name: str = Form(...), steps: List[MacroStep] = Body(...)):
    try:
        if not validate_macro(steps):
            return JSONResponse(status_code=400, content={"error": "Invalid macro steps"})
        save_macro(name, steps)
        return {"status": f"macro '{name}' saved"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/macro/list")
def api_list_macros():
    try:
        return {"macros": list_macros()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/macro/load")
def api_load_macro(name: str = Query(...)):
    try:
        steps = load_macro(name)
        if steps:
            return {"name": name, "steps": steps}
        return JSONResponse(status_code=404, content={"error": "Macro not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/macro/run")
def api_run_saved_macro(name: str = Form(...)):
    try:
        run_saved_macro(name)
        return {"status": f"macro '{name}' executed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/macro/summary")
def api_summarize_macro(steps: List[MacroStep] = Body(...)):
    try:
        if not validate_macro(steps):
            return JSONResponse(status_code=400, content={"error": "Invalid macro steps"})
        return {"summary": summarize_macro(steps)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})