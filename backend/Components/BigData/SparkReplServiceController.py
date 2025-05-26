from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from SparkReplServiceHelper import (
    execute_python_code,
    evaluate_expression,
    get_variable_value
)

app = FastAPI()

@app.post("/spark/repl/exec")
def api_execute_python_code(
    session_id: str = Query(...),
    code: str = Body(..., embed=True)
):
    try:
        result = execute_python_code(session_id, code)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/spark/repl/eval")
def api_evaluate_expression(
    session_id: str = Query(...),
    expression: str = Body(..., embed=True)
):
    try:
        result = evaluate_expression(session_id, expression)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/spark/repl/var")
def api_get_variable_value(
    session_id: str = Query(...),
    var_name: str = Query(...)
):
    try:
        result = get_variable_value(session_id, var_name)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
