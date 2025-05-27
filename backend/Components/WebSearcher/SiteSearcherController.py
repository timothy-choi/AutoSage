from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from SiteSearcherHelper import (
    site_search_google,
    site_search_bing,
    site_search_duckduckgo
)

app = FastAPI()

@app.get("/site-search/google")
def api_site_search_google(
    query: str = Query(...),
    site: str = Query(...),
    api_key: str = Query(...),
    cse_id: str = Query(...),
    max_results: int = Query(10)
):
    try:
        results = site_search_google(query, site, api_key, cse_id, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/site-search/bing")
def api_site_search_bing(
    query: str = Query(...),
    site: str = Query(...),
    api_key: str = Query(...),
    max_results: int = Query(10)
):
    try:
        results = site_search_bing(query, site, api_key, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/site-search/duckduckgo")
def api_site_search_duckduckgo(
    query: str = Query(...),
    site: str = Query(...),
    max_results: int = Query(10)
):
    try:
        results = site_search_duckduckgo(query, site, max_results)
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
