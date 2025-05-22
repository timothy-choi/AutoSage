from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from PluginLoaderHelper import (
    load_plugin,
    list_plugins,
    is_plugin_loaded,
    get_loaded_plugins,
    unload_plugin,
    execute_plugin_function
)

app = FastAPI()

@app.get("/plugins/list")
def api_list_plugins():
    try:
        return {"available_plugins": list_plugins()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/plugins/load")
def api_load_plugin(name: str = Query(...)):
    try:
        result = load_plugin(name)
        if result:
            return {"status": f"Plugin '{name}' loaded."}
        return JSONResponse(status_code=404, content={"error": "Plugin not found or failed to load."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/plugins/loaded")
def api_get_loaded_plugins():
    try:
        return {"loaded_plugins": get_loaded_plugins()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/plugins/is-loaded")
def api_is_plugin_loaded(name: str = Query(...)):
    try:
        return {"loaded": is_plugin_loaded(name)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/plugins/unload")
def api_unload_plugin(name: str = Query(...)):
    try:
        success = unload_plugin(name)
        if success:
            return {"status": f"Plugin '{name}' unloaded."}
        return JSONResponse(status_code=404, content={"error": "Plugin not loaded."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/plugins/execute")
def api_execute_plugin_function(
    plugin_name: str = Query(...),
    function_name: str = Query(...),
    args: list = Body(default=[]),
    kwargs: dict = Body(default={})
):
    try:
        result = execute_plugin_function(plugin_name, function_name, *args, **kwargs)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})