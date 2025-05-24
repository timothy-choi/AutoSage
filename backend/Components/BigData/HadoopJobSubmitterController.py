from fastapi import FastAPI, Form, Body
from fastapi.responses import JSONResponse
from typing import Optional, List
from HadoopJobSubmitterHelper import submit_hadoop_job

app = FastAPI()

@app.post("/hadoop/job/submit")
def api_submit_hadoop_job(
    jar_path: str = Form(...),
    input_path: str = Form(...),
    output_path: str = Form(...),
    main_class: Optional[str] = Form(None),
    additional_args: Optional[List[str]] = Body(default=None)
):
    try:
        output = submit_hadoop_job(
            jar_path=jar_path,
            main_class=main_class,
            input_path=input_path,
            output_path=output_path,
            additional_args=additional_args
        )
        return {"output": output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})