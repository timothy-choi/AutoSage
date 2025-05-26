from fastapi import FastAPI, Form, Query, Body
from fastapi.responses import JSONResponse
from typing import Dict
from HadoopInstanceManagerHelper import (
    create_hadoop_instance,
    delete_hadoop_instance,
    list_hadoop_instances,
    update_hadoop_instance_config
)

app = FastAPI()

@app.post("/hadoop/instance/create")
def api_create_hadoop_instance(config_template_dir: str = Form(...)):
    try:
        instance_id = create_hadoop_instance(config_template_dir)
        return {"instance_id": instance_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/hadoop/instance/delete")
def api_delete_hadoop_instance(instance_id: str = Query(...)):
    try:
        success = delete_hadoop_instance(instance_id)
        return {"status": "deleted" if success else "not found"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/hadoop/instance/list")
def api_list_hadoop_instances():
    try:
        instances = list_hadoop_instances()
        return {"instances": instances}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.put("/hadoop/instance/update-config")
def api_update_hadoop_instance_config(
    instance_id: str = Query(...),
    file_name: str = Query(...),
    updates: Dict[str, str] = Body(...)
):
    try:
        success = update_hadoop_instance_config(instance_id, file_name, updates)
        return {"status": "updated" if success else "not found or failed"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})