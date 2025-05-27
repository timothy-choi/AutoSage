from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from WebSearcherHelper import (
    search_web_duckduckgo_api,
    search_web_bing,
    search_web_google
)

app = FastAPI()

@app.get("/search/duckduckgo")
def api_search_duckduckgo(query: str = Query(...), max_results: int = Query(10)):
    try:
        results = search_web_duckduckgo_api(query, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/search/bing")
def api_search_bing(query: str = Query(...), api_key: str = Query(...), max_results: int = Query(10)):
    try:
        results = search_web_bing(query, api_key, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/search/google")
def api_search_google(query: str = Query(...), api_key: str = Query(...), cse_id: str = Query(...), max_results: int = Query(10)):
    try:
        results = search_web_google(query, api_key, cse_id, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
