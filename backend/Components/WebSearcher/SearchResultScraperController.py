from fastapi import FastAPI, Query
from SearchResultScraperHelper import scrape_search_results

app = FastAPI()

@app.get("/scrape-search")
def scrape_search_endpoint(
    url: str = Query(..., description="URL of the search results page"),
    max_results: int = Query(10, description="Maximum number of results to return")
):
    try:
        return {"results": scrape_search_results(url, max_results)}
    except Exception as e:
        return {"error": str(e)}